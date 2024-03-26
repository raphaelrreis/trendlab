package br.com.desafio.payments.dto;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class PaymentDTOTest {

    @Test
    void testPaymentDTO() {
        PaymentDTO paymentDTO = new PaymentDTO();
        paymentDTO.setClientId("123456");
        paymentDTO.setPaymentItems(null);

        assertEquals("123456", paymentDTO.getClientId());
        assertNull(paymentDTO.getPaymentItems());
    }
}
