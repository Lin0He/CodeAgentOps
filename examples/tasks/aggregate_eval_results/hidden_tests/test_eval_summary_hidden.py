from eval_summary import aggregate_eval_results


def test_missing_fields_are_handled():
    results = [
        {"success": True, "iterations": 2},
        {"public_passed": True, "cost_usd": 0.05},
        {"hidden_passed": True, "latency_s": 3.0},
    ]

    summary = aggregate_eval_results(results)

    assert summary["tasks"] == 3
    assert summary["successes"] == 1
    assert summary["success_rate"] == 1 / 3
    assert summary["public_pass_rate"] == 1 / 3
    assert summary["hidden_pass_rate"] == 1 / 3
    assert summary["avg_iterations"] == 2 / 3
    assert summary["total_cost_usd"] == 0.05
    assert summary["avg_latency_s"] == 1.0


def test_false_values_are_not_counted():
    results = [
        {"success": False, "public_passed": False, "hidden_passed": False},
        {"success": True, "public_passed": True, "hidden_passed": False},
    ]

    summary = aggregate_eval_results(results)

    assert summary["successes"] == 1
    assert summary["success_rate"] == 0.5
    assert summary["public_pass_rate"] == 0.5
    assert summary["hidden_pass_rate"] == 0.0