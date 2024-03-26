package br.com.desafio.payments.dto;

import lombok.*;

import java.math.BigDecimal;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class PaymentItemDTO {
    private String paymentId;
    private BigDecimal paymentValue;
    private String paymentStatus;
}
