package thkim.mystocks.stockService.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import thkim.mystocks.stockService.component.KisComponent;
import thkim.mystocks.stockService.entity.StockListEntity;
import thkim.mystocks.stockService.repository.StockListRepository;

import java.util.List;


@Slf4j
@Service
public class TestService {
    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    StockListRepository stockListRepository;

    @Autowired
    KisComponent kisComponent;


    public void testRestTemplate() {
        List<StockListEntity> stockListEntityList = stockListRepository.findAll();
        for (StockListEntity stockListEntity : stockListEntityList) {
            log.info("## testRestTemplate(): {}", stockListEntity.getScode());
        }

//        String res = restTemplate.postForObject("", "", String.class);
        String res = restTemplate.getForObject("http://localhost:9001/lotto", String.class);
        log.info("## testRestTemplate(): rest {}", res);

    }

    public void test01() {
        log.info("TestService: test01(): 실행");
        kisComponent.login();
    }
}
