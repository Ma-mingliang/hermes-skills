#!/usr/bin/env python3
"""
Hindsight health monitor — 4-point end-to-end check.

Usage:
    python monitor.py                    # print report to stdout
    python monitor.py --json             # JSON output for automation
    python monitor.py --store            # also test memory storage
    python monitor.py --reflect          # also test LLM-powered reflect

Environment (optional):
    HINDSIGHT_URL   API base URL (default http://localhost:8888)
    HINDSIGHT_BANK  Bank ID (default hermes)
    TIMEOUT_SEC     HTTP timeout (default 30)

Exit codes: 0=healthy, 1=degraded, 2=down.
"""

import json, os, sys, urllib.request, urllib.error, time, argparse
from datetime import datetime, timezone

BASE = os.environ.get("HINDSIGHT_URL", "http://localhost:8888")
BANK = os.environ.get("HINDSIGHT_BANK", "hermes")
TIMEOUT = int(os.environ.get("TIMEOUT_SEC", "30"))


def api_get(path, timeout=TIMEOUT):
    req = urllib.request.Request(f"{BASE}{path}")
    req.add_header("User-Agent", "Hindsight-Monitor/1.0")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read())


def api_post(path, data, timeout=TIMEOUT):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Hindsight-Monitor/1.0")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read())


def check_port(host="127.0.0.1", port=8888):
    """TCP connect check — works even if HTTP layer is down."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def sample_metrics():
    """Extract key counters from Prometheus /metrics."""
    try:
        _, raw = api_get("/metrics")
        if isinstance(raw, dict):
            # Some versions return JSON
            return raw
        lines = raw.split("\n") if isinstance(raw, str) else []
        out = {}
        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            # Simple extraction: hindsight_llm_calls_total{...} 10.0
            if "hindsight_llm_calls_total" in line and 'success="true"' in line:
                scope = line.split('scope="')[1].split('"')[0] if 'scope="' in line else "?"
                val = float(line.split()[-1])
                out[f"llm_calls_{scope}"] = int(val)
            elif "hindsight_http_requests_total" in line and 'status_class="2xx"' in line:
                endpoint = line.split('endpoint="')[1].split('"')[0] if 'endpoint="' in line else "?"
                val = float(line.split()[-1])
                out[f"http_2xx_{endpoint}"] = int(val)
            elif "hindsight_db_pool_size" in line:
                out["db_pool_size"] = int(float(line.split()[-1]))
            elif "hindsight_process_threads" in line:
                out["process_threads"] = int(float(line.split()[-1]))
        return out
    except Exception as e:
        return {"error": str(e)[:120]}


def run_checks(args):
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE,
        "bank_id": BANK,
        "checks": {},
    }
    status = "healthy"
    exit_code = 0

    # --- 1. Port probe ---
    t0 = time.time()
    port_ok = check_port()
    results["checks"]["port"] = {
        "ok": port_ok,
        "latency_ms": round((time.time() - t0) * 1000, 1),
    }
    if not port_ok:
        results["checks"]["port"]["error"] = "TCP connect refused"
        status = "down"
        exit_code = 2

    # --- 2. Health endpoint ---
    try:
        t0 = time.time()
        code, health = api_get("/health")
        results["checks"]["health"] = {
            "ok": code == 200 and health.get("status") == "healthy",
            "http_status": code,
            "body": health,
            "latency_ms": round((time.time() - t0) * 1000, 1),
        }
        if code != 200:
            status = "down"
            exit_code = 2
    except Exception as e:
        results["checks"]["health"] = {"ok": False, "error": str(e)[:200]}
        status = "down"
        exit_code = 2

    # --- 2b. Version info ---
    try:
        _, ver = api_get("/version")
        results["checks"]["version"] = {
            "ok": True,
            "api_version": ver.get("api_version", "?"),
            "features": ver.get("features", {}),
        }
    except Exception:
        pass

    if exit_code == 2:
        return results, status, exit_code

    # --- 3. API surface (endpoint discovery) ---
    try:
        t0 = time.time()
        code, spec = api_get("/openapi.json")
        paths = list(spec.get("paths", {}).keys())
        mem_store = any(f"/banks/{{bank_id}}/memories" in p for p in paths)
        mem_recall = any("memories/recall" in p for p in paths)
        results["checks"]["api_surface"] = {
            "ok": mem_store and mem_recall,
            "version": spec.get("info", {}).get("version", "?"),
            "endpoint_count": len(paths),
            "memory_store_endpoint": mem_store,
            "memory_recall_endpoint": mem_recall,
            "latency_ms": round((time.time() - t0) * 1000, 1),
        }
    except Exception as e:
        results["checks"]["api_surface"] = {"ok": False, "error": str(e)[:200]}
        status = "degraded"
        exit_code = max(exit_code, 1)

    # --- 4. Bank stats ---
    try:
        t0 = time.time()
        code, stats = api_get(f"/v1/default/banks/{BANK}/stats")
        results["checks"]["stats"] = {
            "ok": code == 200,
            "total_nodes": stats.get("total_nodes"),
            "total_documents": stats.get("total_documents"),
            "failed_operations": stats.get("failed_operations", 0),
            "pending_operations": stats.get("pending_operations", 0),
            "last_consolidated_at": stats.get("last_consolidated_at"),
            "latency_ms": round((time.time() - t0) * 1000, 1),
        }
        if stats.get("failed_operations", 0) > 0:
            status = "degraded"
            exit_code = max(exit_code, 1)
    except Exception as e:
        results["checks"]["stats"] = {"ok": False, "error": str(e)[:200]}
        status = "degraded"
        exit_code = max(exit_code, 1)

    # --- 5. Memory retrieval (lightweight) ---
    try:
        t0 = time.time()
        code, recall = api_post(
            f"/v1/default/banks/{BANK}/memories/recall",
            {"query": "health check monitoring status", "max_tokens": 500, "budget": "low"},
            timeout=60,
        )
        n_results = len(recall.get("results", []))
        results["checks"]["recall"] = {
            "ok": code == 200,  # 200 is sufficient — bank may be empty
            "result_count": n_results,
            "latency_ms": round((time.time() - t0) * 1000, 1),
        }
    except Exception as e:
        results["checks"]["recall"] = {"ok": False, "error": str(e)[:200]}
        status = "degraded"
        exit_code = max(exit_code, 1)

    # --- 6. Memory storage (optional) ---
    if args.store:
        try:
            t0 = time.time()
            code, store = api_post(
                f"/v1/default/banks/{BANK}/memories",
                {
                    "items": [{
                        "content": "Hindsight自动巡检 — 系统健康检查记忆",
                        "metadata": {"source": "monitor_cron", "date": datetime.now().isoformat()[:10]},
                    }]
                },
                timeout=90,
            )
            results["checks"]["store"] = {
                "ok": code == 200 and store.get("success"),
                "items_count": store.get("items_count", 0),
                "tokens": store.get("usage", {}).get("total_tokens", 0),
                "latency_ms": round((time.time() - t0) * 1000, 1),
            }
        except Exception as e:
            results["checks"]["store"] = {"ok": False, "error": str(e)[:200]}
            status = "degraded"
            exit_code = max(exit_code, 1)

    # --- 7. Reflect / LLM backend (optional) ---
    if args.reflect:
        try:
            t0 = time.time()
            code, reflect = api_post(
                f"/v1/default/banks/{BANK}/reflect",
                {"query": "Summarize current system status in one sentence.", "budget": "low"},
                timeout=90,
            )
            text_len = len(reflect.get("text", "")) if isinstance(reflect, dict) else 0
            results["checks"]["reflect"] = {
                "ok": code == 200 and text_len > 0,
                "text_length": text_len,
                "latency_ms": round((time.time() - t0) * 1000, 1),
            }
        except Exception as e:
            results["checks"]["reflect"] = {"ok": False, "error": str(e)[:200]}
            status = "degraded"
            exit_code = max(exit_code, 1)

    # --- 8. Metrics sampling ---
    try:
        metrics = sample_metrics()
        results["checks"]["metrics"] = {"ok": "error" not in metrics, **metrics}
    except Exception:
        pass

    # --- 9. Model verification (check configured model exists on provider) ---\n    try:\n        env_file = os.path.expanduser(\"~/.hindsight/.env\")\n        if os.path.exists(env_file):\n            env = {}\n            with open(env_file) as f:\n                for line in f:\n                    if \"=\" in line and not line.startswith(\"#\"):\n                        k, v = line.strip().split(\"=\", 1)\n                        env[k] = v\n            base_url = env.get(\"HINDSIGHT_API_LLM_BASE_URL\", \"\")\n            api_key = env.get(\"HINDSIGHT_API_LLM_API_KEY\", \"\")\n            configured_model = env.get(\"HINDSIGHT_API_LLM_MODEL\", \"gpt-4o-mini (default)\")\n            if base_url and api_key:\n                req = urllib.request.Request(f\"{base_url}/models\")\n                req.add_header(\"Authorization\", f\"Bearer {api_key}\")\n                models_resp = json.loads(urllib.request.urlopen(req, timeout=10).read())\n                available = [m[\"id\"] for m in models_resp.get(\"data\", [])]\n                model_ok = configured_model in available\n                results[\"checks\"][\"model\"] = {\n                    \"ok\": model_ok,\n                    \"configured\": configured_model,\n                    \"available_count\": len(available),\n                    \"match\": model_ok,\n                }\n                if not model_ok:\n                    status = \"degraded\"\n                    exit_code = max(exit_code, 1)\n    except Exception as e:\n        results[\"checks\"][\"model\"] = {\"ok\": False, \"error\": str(e)[:200]}\n\n    results[\"status\"] = status\n    return results, status, exit_code


def format_report(results, status):
    """Human-readable report for cron delivery."""
    lines = []
    lines.append("# Hindsight 监控报告")
    lines.append(f"**时间**: {results['timestamp']}")
    lines.append(f"**服务**: {results['base_url']} | Bank: {results['bank_id']} | 状态: {status}")
    lines.append("")

    checks = results.get("checks", {})
    for name, c in checks.items():
        if c is None:
            continue
        icon = "✅" if c.get("ok") else "❌"
        if name == "port":
            lines.append(f"**端口探测**: {icon} ({c.get('latency_ms', '?')}ms)")
        elif name == "health":
            body = c.get("body", {})
            lines.append(f"**健康检查**: {icon} {body.get('status','?')} | DB: {body.get('database','?')} ({c.get('latency_ms','?')}ms)")
        elif name == "version":
            lines.append(f"**版本**: {icon} v{c.get('api_version','?')} | features: {', '.join(k for k,v in c.get('features',{}).items() if v)}")
        elif name == "api_surface":
            lines.append(f"**API表面**: {icon} v{c.get('version','?')} | {c.get('endpoint_count','?')} 端点 | store={c.get('memory_store_endpoint')} recall={c.get('memory_recall_endpoint')}")
        elif name == "stats":
            lines.append(f"**银行统计**: {icon} {c.get('total_nodes','?')} 节点 | {c.get('total_documents','?')} 文档 | 失败={c.get('failed_operations','?')} 待定={c.get('pending_operations','?')}")
        elif name == "recall":
            lines.append(f"**记忆检索**: {icon} {c.get('result_count','?')} 条结果 ({c.get('latency_ms','?')}ms)")
        elif name == "store":
            lines.append(f"**记忆存储**: {icon} {c.get('items_count','?')} 条 | {c.get('tokens','?')} tokens")
        elif name == "reflect":
            lines.append(f"**Reflect (LLM)**: {icon} {c.get('text_length','?')} 字符 ({c.get('latency_ms','?')}ms)")
        elif name == "metrics":
            m = {k: v for k, v in c.items() if k != "ok"}
            if m:
                parts = [f"{k}={v}" for k, v in sorted(m.items())]
                lines.append(f"**指标抽样**: {icon} {' | '.join(parts[:8])}")
        elif name == "model":
            lines.append(f"**模型验证**: {icon} configured={c.get('configured','?')} | available={c.get('available_count','?')} | match={c.get('match','?')}")
        else:
            error = c.get("error", "")
            if error:
                lines.append(f"**{name}**: {icon} {error[:120]}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Hindsight health monitor")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--store", action="store_true", help="Test memory storage (LLM-backed, slow)")
    parser.add_argument("--reflect", action="store_true", help="Test LLM reflect endpoint")
    args = parser.parse_args()

    results, status, exit_code = run_checks(args)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_report(results, status))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
