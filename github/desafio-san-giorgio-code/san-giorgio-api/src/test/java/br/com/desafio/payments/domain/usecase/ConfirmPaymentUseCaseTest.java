package br.com.desafio.payments.domain.usecase;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.repository.PaymentRepository;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@SpringBootTest
class ConfirmPaymentUseCaseTest {

    @Mock
    private PaymentRepository paymentRepository;


    @InjectMocks
    private ConfirmPaymentUseCaseImpl confirmPaymentUseCase;

    @Test
    void testConfirmPayment() {
        PaymentModel paymentModel = new PaymentModel();

        when(paymentRepository.existsBySellerIdAndBillingCode(anyLong(), anyString())).thenReturn(false);
        when(paymentRepository.save(any())).thenReturn(paymentModel);

        PaymentModel confirmedPayment = confirmPaymentUseCase.confirmPayment(paymentModel);

        assertNotNull(confirmedPayment);
    }
}
