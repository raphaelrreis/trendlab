package br.com.desafio.payments.domain.service;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.repository.PaymentRepository;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class PaymentServiceTest {

    @Test
    void testGetPaymentByBillingCode() {
        PaymentRepository paymentRepository = mock(PaymentRepository.class);

        String billingCode = "code123";
        PaymentModel expectedPayment = createPaymentModel(123L, billingCode, BigDecimal.TEN);

        when(paymentRepository.findByBillingCode(billingCode)).thenReturn(expectedPayment);

        PaymentService paymentService = new PaymentService(paymentRepository);

        PaymentModel actualPayment = paymentService.getPaymentByBillingCode(billingCode);

        assertEquals(expectedPayment, actualPayment);
    }

    @Test
    void testGetPaymentsBySellerId() {
        PaymentRepository paymentRepository = mock(PaymentRepository.class);

        Long sellerId = 123L;
        PaymentModel payment1 = createPaymentModel(sellerId, "code1", BigDecimal.TEN);
        PaymentModel payment2 = createPaymentModel(sellerId, "code2", BigDecimal.ONE);
        List<PaymentModel> expectedPayments = Arrays.asList(payment1, payment2);

        when(paymentRepository.findBySellerId(sellerId)).thenReturn(expectedPayments);

        PaymentService paymentService = new PaymentService(paymentRepository);

        List<PaymentModel> actualPayments = paymentService.getPaymentsBySellerId(sellerId);
        assertEquals(expectedPayments, actualPayments);
    }


    private PaymentModel createPaymentModel(Long sellerId, String billingCode, BigDecimal paymentValue) {
        PaymentModel paymentModel = new PaymentModel();
        paymentModel.setSellerId(sellerId);
        paymentModel.setBillingCode(billingCode);
        paymentModel.setStatus("PENDING");
        return paymentModel;
    }
}
