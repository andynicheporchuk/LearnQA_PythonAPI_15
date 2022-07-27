import requests, pytest

class TestAPI:

    userAgents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    ]

    @pytest.mark.parametrize('UserAgent', userAgents)


    def test_user_agent(self, UserAgent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {
            "User-Agent": UserAgent
        }
        response = requests.get(url, headers = headers)

        assert "platform" in response.text, "Response has not field 'platform'"
        assert "device" in response.text, "Response has not field 'device'"
        assert "browser" in response.text, "Response has not field 'browser'"

        expectedResults = [
            '"platform":"Mobile","browser":"No","device":"Android"',
            '"platform":"Mobile","browser":"Chrome","device":"iOS"',
            '"platform":"Googlebot","browser":"Unknown","device":"Unknown"',
            '"platform":"Web","browser":"Chrome","device":"No"',
            '"platform":"Mobile","browser":"No","device":"iPhone"'
        ]

        if UserAgent == "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30":
            expectedResult = expectedResults[0]
        elif UserAgent == "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1":
            expectedResult = expectedResults[1]
        elif UserAgent == "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)":
            expectedResult = expectedResults[2]
        elif UserAgent == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0":
            expectedResult = expectedResults[3]
        elif UserAgent == "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1":
            expectedResult = expectedResults[4]
        else:
            expectedResult = False

        assert expectedResult in response.text, f"There is no expected result in the response for User-Agent = {UserAgent}"



