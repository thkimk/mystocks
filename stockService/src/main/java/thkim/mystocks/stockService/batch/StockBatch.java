package thkim.mystocks.stockService.batch;


import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import thkim.mystocks.stockService.service.TestService;

import java.util.List;
import java.util.Optional;

@Configuration
@EnableScheduling
@Component
@Slf4j
public class StockBatch {
    @Autowired
    TestService testService;

//    @Scheduled(fixedDelay = 1000)
    public void test01() {
        log.info("## [CALLED] StockBatch: run()..................................................");

        testService.testRestTemplate();

    }

//    @Scheduled(fixedRate = 2000, initialDelay = 3000)
    public void test02() {
        log.info("Scheduler 실행");
    }
}
