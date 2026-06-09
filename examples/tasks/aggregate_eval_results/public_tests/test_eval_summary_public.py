from eval_summary import aggregate_eval_results


def test_aggregates_basic_metrics():
    results = [
        {
            "success": True,
            "public_passed": True,
            "hidden_passed": True,
            "iterations": 1,
            "cost_usd": 0.01,
            "latency_s": 2.0,
        },
        {
            "success": False,
            "public_passed": True,
            "hidden_passed": False,
            "iterations": 3,
            "cost_usd": 0.03,
            "latency_s": 6.0,
        },
    ]

    summary = aggregate_eval_results(results)

    assert summary["tasks"] == 2
    assert summary["successes"] == 1
    assert summary["success_rate"] == 0.5
    assert summary["public_pass_rate"] == 1.0
    assert summary["hidden_pass_rate"] == 0.5
    assert summary["avg_iterations"] == 2.0
    assert summary["total_cost_usd"] == 0.04
    assert summary["avg_latency_s"] == 4.0


def test_empty_results():
    summary = aggregate_eval_results([])

    assert summary["tasks"] == 0
    assert summary["successes"] == 0
    assert summary["success_rate"] == 0.0
    assert summary["public_pass_rate"] == 0.0
    assert summary["hidden_pass_rate"] == 0.0
    assert summary["avg_iterations"] == 0.0
    assert summary["total_cost_usd"] == 0.0
    assert summary["avg_latency_s"] == 0.0