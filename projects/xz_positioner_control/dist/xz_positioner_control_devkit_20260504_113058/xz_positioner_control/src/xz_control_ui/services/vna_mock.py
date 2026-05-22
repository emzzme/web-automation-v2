class VnaClientMock:
    def connect(self) -> bool:
        return True

    def fetch_s21_trace(self) -> list[float]:
        return []
