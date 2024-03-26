package br.com.desafio.payments.domain.model;

import br.com.desafio.payments.dto.PaymentItemDTO;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class PaymentModelTest {

    @Test
    void testPaymentModelCreation() {
        Long id = 1L;
        Long sellerId = 1001L;
        String billingCode = "BILL123";
        String status = "CONFIRMED";
        List<PaymentItemDTO> items = new ArrayList<>();

        PaymentModel paymentModel = PaymentModel.builder()
                .id(id)
                .sellerId(sellerId)
                .billingCode(billingCode)
                .status(status)
                .items(items)
                .build();

        assertNotNull(paymentModel);
        assertEquals(id, paymentModel.getId());
        assertEquals(sellerId, paymentModel.getSellerId());
        assertEquals(billingCode, paymentModel.getBillingCode());
        assertEquals(status, paymentModel.getStatus());
        assertEquals(items, paymentModel.getItems());
    }
}
