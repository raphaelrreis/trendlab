package br.com.desafio.payments.dto;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
@ContextConfiguration(classes = PaymentItemDTOTest.TestConfig.class)
class PaymentItemDTOTest {

    @Test
    void testPaymentItemDTO() {
        PaymentItemDTO itemDTO = PaymentItemDTO.builder()
                .paymentId("123")
                .paymentValue(BigDecimal.TEN)
                .paymentStatus("CONFIRMED")
                .build();

        assertEquals("123", itemDTO.getPaymentId());
        assertEquals(BigDecimal.TEN, itemDTO.getPaymentValue());
        assertEquals("CONFIRMED", itemDTO.getPaymentStatus());
    }

}
