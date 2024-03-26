package br.com.desafio.payments.controller;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.service.PaymentService;
import br.com.desafio.payments.exception.InvalidPaymentException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

class PaymentControllerTest {

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private PaymentController paymentController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    void testProcessPayment_InvalidPayment() {
        // Arrange
        PaymentModel invalidPayment = new PaymentModel();
        invalidPayment.setStatus("INVALID");

        // Define o comportamento do serviço mockado
        when(paymentService.processPayment(invalidPayment)).thenThrow(new InvalidPaymentException("Pagamento inválido"));

        // Act e Assert
        assertThrows(InvalidPaymentException.class, () -> {
            paymentController.processPayment(invalidPayment);
        });
    }
}
