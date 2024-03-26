package br.com.desafio.payments.exception;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class InvalidPaymentExceptionTest {

    @Test
    void testInvalidPaymentException() {
        String errorMessage = "Invalid payment exception message";

        InvalidPaymentException exception = new InvalidPaymentException(errorMessage);

        assertNotNull(exception);
        assertEquals(errorMessage, exception.getMessage());
    }
}
