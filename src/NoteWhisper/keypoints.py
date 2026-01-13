class KeypointExtractor:
    def extract(self, text: str) -> list[str]:
        """Dummy keypoint extraction"""
        lines = [line.strip() for line in text.split(".") if line.strip()]
        return lines[:5]  # return first 5 sentences as keypoints
