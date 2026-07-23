from src.mock_data import (
    get_mock_analogues,
    get_mock_articles,
    get_mock_predictions,
    get_mock_prices,
)


def test_mock_articles_exist():
    articles = get_mock_articles()
    assert len(articles) >= 5
    assert all(article.title for article in articles)


def test_all_prediction_horizons_exist():
    frame = get_mock_predictions("news-001")
    assert frame["Horizon"].tolist() == ["1D", "3D", "5D", "10D", "20D"]
    assert frame["Probability"].between(0, 1).all()


def test_analogue_similarities_are_valid():
    frame = get_mock_analogues("news-001")
    assert len(frame) >= 10
    assert frame["Text similarity"].between(0, 1).all()
    assert frame["Regime similarity"].between(0, 1).all()


def test_mock_prices_are_positive_and_ordered():
    frame = get_mock_prices("GOOGL")
    assert not frame.empty
    assert frame["date"].is_monotonic_increasing
    assert (frame["close"] > 0).all()
