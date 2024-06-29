package thkim.mystocks.stockService.entity;


import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.time.LocalDate;

@NoArgsConstructor
@Entity
@Data
@Table(name = "stock_list")
public class StockListEntity {
    @Id
    private String scode;

    private String sname;
    private String stype;
    private String state;

}
