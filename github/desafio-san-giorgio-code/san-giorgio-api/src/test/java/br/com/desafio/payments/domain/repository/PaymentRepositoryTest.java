package br.com.desafio.payments.domain.repository;

import br.com.desafio.payments.domain.model.PaymentModel;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class PaymentRepositoryTest {

    @Test
    void testFindBySellerId() {
        PaymentRepository paymentRepository = mock(PaymentRepository.class);

        Long sellerId = 123L;
        PaymentModel paymentModel1 = createPaymentModel(sellerId, "code1", BigDecimal.TEN);
        PaymentModel paymentModel2 = createPaymentModel(sellerId, "code2", BigDecimal.ONE);
        List<PaymentModel> expectedPayments = Arrays.asList(paymentModel1, paymentModel2);

        when(paymentRepository.findBySellerId(sellerId)).thenReturn(expectedPayments);

        List<PaymentModel> actualPayments = paymentRepository.findBySellerId(sellerId);

        assertEquals(expectedPayments.size(), actualPayments.size());
        assertEquals(expectedPayments.get(0).getSellerId(), actualPayments.get(0).getSellerId());
        assertEquals(expectedPayments.get(1).getSellerId(), actualPayments.get(1).getSellerId());
    }

    private PaymentModel createPaymentModel(Long sellerId, String billingCode, BigDecimal paymentValue) {
        PaymentModel paymentModel = new PaymentModel();
        paymentModel.setSellerId(sellerId);
        paymentModel.setBillingCode(billingCode);
        paymentModel.setStatus("PENDING");
        return paymentModel;
    }
}
