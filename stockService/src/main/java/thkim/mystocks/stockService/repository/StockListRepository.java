package thkim.mystocks.stockService.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import thkim.mystocks.stockService.entity.StockListEntity;

import java.util.List;

public interface StockListRepository extends JpaRepository<StockListEntity, String> {
    //

}
