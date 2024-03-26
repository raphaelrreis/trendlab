package br.com.desafio.payments.domain.usecase;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.repository.PaymentRepository;
import br.com.desafio.payments.domain.service.SqsService;
import br.com.desafio.payments.dto.PaymentItemDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@SpringBootTest
@ContextConfiguration(classes = ConfirmPaymentUseCaseImplTest.TestConfig.class)
class ConfirmPaymentUseCaseImplTest {

    @Configuration
    static class TestConfig {
        @Bean
        public String queueUrl(@Value("${cloud.aws.sqs.queue.partial-payments}") String queueUrl) {
            return queueUrl;
        }
    }


    @Mock
    private PaymentRepository paymentRepository;

    @Mock
    private SqsService sqsService;

    @InjectMocks
    private ConfirmPaymentUseCaseImpl paymentUseCase;

    @Value("${cloud.aws.sqs.queue.partial-payments}")
    private String queueUrl;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void confirmPayment_NewPayment_Success() {
        // Arrange
        PaymentModel paymentModel = createPaymentModel("123", "456", BigDecimal.TEN);
        when(paymentRepository.existsBySellerIdAndBillingCode(anyLong(), anyString())).thenReturn(false);
        when(paymentRepository.save(any())).thenReturn(paymentModel);

        // Act
        PaymentModel confirmedPayment = paymentUseCase.confirmPayment(paymentModel);

        // Assert
        assertNotNull(confirmedPayment);
        assertEquals("CONFIRMED", confirmedPayment.getStatus());
        assertEquals(1, confirmedPayment.getItems().size());
        assertEquals("CONFIRMED", confirmedPayment.getItems().get(0).getPaymentStatus());
        verify(paymentRepository, times(1)).save(any());
        verify(sqsService, times(1)).sendPaymentMessage(anyString(), anyString());
    }

    // Restante do teste não alterado

    private PaymentModel createPaymentModel(String sellerId, String billingCode, BigDecimal paymentValue) {
        PaymentModel paymentModel = new PaymentModel();
        paymentModel.setSellerId(Long.valueOf(sellerId));
        paymentModel.setBillingCode(billingCode);
        paymentModel.setStatus("PENDING");
        List<PaymentItemDTO> items = new ArrayList<>();
        PaymentItemDTO item = new PaymentItemDTO();
        item.setPaymentValue(paymentValue);
        items.add(item);
        paymentModel.setItems(items);
        return paymentModel;
    }
}
