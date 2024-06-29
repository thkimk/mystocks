package thkim.mystocks.stockService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import thkim.mystocks.stockService.config.ApplicationContextProvider;
import thkim.mystocks.stockService.service.TestService;

import javax.el.BeanNameResolver;

@SpringBootApplication
public class StockServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(StockServiceApplication.class, args);

		TestService testService = ApplicationContextProvider.getBean("testService", TestService.class);
		testService.test01();
	}

}
