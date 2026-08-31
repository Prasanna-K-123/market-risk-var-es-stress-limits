from src.stress import hypothetical_stress_table


def test_hypothetical_stresses_have_losses_and_names():
    table = hypothetical_stress_table()
    assert table["scenario"].nunique() >= 4
    assert table["loss"].max() > 0
