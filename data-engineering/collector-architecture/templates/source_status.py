#!/usr/bin/env python3
"""
Unified source_status module for multi-source collectors.
All collectors must return (items, source_status) tuples.
"""

from typing import List, Dict, Any, Tuple

# 9 status enums
STATUS_SUCCESS = "success"
STATUS_SUCCESS_NO_MATCH = "success_no_match"
STATUS_CHECKED_NO_CHANGE = "checked_no_change"
STATUS_SKIPPED_DISABLED = "skipped_disabled"
STATUS_SKIPPED_MISSING_AUTH = "skipped_missing_auth"
STATUS_FAILED_NETWORK = "failed_network"
STATUS_FAILED_PARSE = "failed_parse"
STATUS_FAILED_AUTH = "failed_auth"
STATUS_FAILED_RATE_LIMITED = "failed_rate_limited"

VALID_STATUSES = {
    STATUS_SUCCESS, STATUS_SUCCESS_NO_MATCH, STATUS_CHECKED_NO_CHANGE,
    STATUS_SKIPPED_DISABLED, STATUS_SKIPPED_MISSING_AUTH,
    STATUS_FAILED_NETWORK, STATUS_FAILED_PARSE, STATUS_FAILED_AUTH,
    STATUS_FAILED_RATE_LIMITED,
}


def make_source_status(
    source: str,
    enabled: bool = True,
    status: str = STATUS_SUCCESS,
    auth: str = "ok",
    strategy_used: str = "",
    raw_count: int = 0,
    matched_count: int = 0,
    selected_count: int = 0,
    items: List[Dict] = None,
    errors: List[str] = None,
    warnings: List[str] = None,
) -> Dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")
    return {
        "source": source,
        "enabled": enabled,
        "status": status,
        "auth": auth,
        "strategy_used": strategy_used,
        "raw_count": raw_count,
        "matched_count": matched_count,
        "selected_count": selected_count,
        "items": items or [],
        "errors": errors or [],
        "warnings": warnings or [],
    }


def skipped_disabled(source: str) -> Tuple[List[Dict], Dict]:
    return [], make_source_status(source=source, enabled=False, status=STATUS_SKIPPED_DISABLED)


def skipped_missing_auth(source: str, missing_vars: List[str]) -> Tuple[List[Dict], Dict]:
    return [], make_source_status(
        source=source, enabled=True, status=STATUS_SKIPPED_MISSING_AUTH,
        warnings=[f"Missing env vars: {', '.join(missing_vars)}"],
    )


def failed_network(source: str, error: str) -> Tuple[List[Dict], Dict]:
    return [], make_source_status(
        source=source, enabled=True, status=STATUS_FAILED_NETWORK, errors=[error],
    )


def failed_parse(source: str, error: str) -> Tuple[List[Dict], Dict]:
    return [], make_source_status(
        source=source, enabled=True, status=STATUS_FAILED_PARSE, errors=[error],
    )


def failed_auth(source: str, error: str) -> Tuple[List[Dict], Dict]:
    return [], make_source_status(
        source=source, enabled=True, status=STATUS_FAILED_AUTH, errors=[error],
    )


def failed_rate_limited(source: str, error: str = "HTTP 429") -> Tuple[List[Dict], Dict]:
    return [], make_source_status(
        source=source, enabled=True, status=STATUS_FAILED_RATE_LIMITED, errors=[error],
    )
