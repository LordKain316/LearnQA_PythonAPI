class TestPhrase:
    def test_pharse(self):
        a = input("Set a phrase:")
        assert len(a) <= 14, f"Длина фразы превышает ожидаемую"