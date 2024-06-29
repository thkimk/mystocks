package thkim.mystocks.stockService.dto;

import lombok.Data;

@Data
public class KisLoginInDto {
    String grant_type = "client_credentials";
    String appkey;
    String appsecret;
}
