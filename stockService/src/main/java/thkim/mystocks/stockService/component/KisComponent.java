package thkim.mystocks.stockService.component;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import thkim.mystocks.stockService.dto.KisLoginInDto;
import thkim.mystocks.stockService.dto.KisLoginOutDto;

@Slf4j
@Component
public class KisComponent {
    final String APP_Key = "PStmdgpRr3snHex7Xq3V1eCyCKgEeSlSvOrL";
    final String APP_Secret = "QR5v7CkU92i3H0DiryPNc8HP+cWbTUIJ/5ETag2lY54l2yGMkKwlFbfRl+D70zY+1irgRCZbM9AqoVoS2zA1A5+ETJtJer8TxQUW9Voy1CA8qIl8DGnFMnoAVhAgV4W+bG7rqogL8bmWkeoo6c3mH/x6yGnf7aIfpGhtSIlHb2V+TY2bdTE=";

    final String url = "https://openapi.koreainvestment.com:9443";

    @Autowired
    private RestTemplate restTemplate;


    public void login() {
        log.info("## KisComponent: login(): starts..");

        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.add("content-type", "application/json");
        httpHeaders.add("appKey", APP_Key);
        httpHeaders.add("appSecret", APP_Secret);

        KisLoginInDto kisLoginInDto = new KisLoginInDto();
        kisLoginInDto.setAppkey(APP_Key);
        kisLoginInDto.setAppsecret(APP_Secret);

        HttpEntity entity = new HttpEntity(kisLoginInDto, httpHeaders);

        try {
            // 2024-06-29 00:00:58.320 [main] INFO t.m.s.c.KisComponent [] ## login(): eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImFkMTUxNzFiLTdhMmYtNDU2NS04MzI1LWUzNGQ0Zjg0NTJlMCIsInByZHRfY2QiOiIiLCJpc3MiOiJ1bm9ndyIsImV4cCI6MTcxOTY3MzI1OCwiaWF0IjoxNzE5NTg2ODU4LCJqdGkiOiJQU3RtZGdwUnIzc25IZXg3WHEzVjFlQ3lDS2dFZVNsU3ZPckwifQ.WbpuhEoHC2qzGLSRv-upYsBXkcX6yaFwRmRK3yR1pfTHu9OE8Jz_XlGaKF5pOYXuLkxBX75NbKUCyC6OZb0-nw
            KisLoginOutDto res = restTemplate.postForObject(url.concat("/oauth2/tokenP"), entity, KisLoginOutDto.class);
            log.info("## login(): {}", res.getAccess_token());
        } catch (Exception e) {
            log.error("message", e);
        }

    }
}
