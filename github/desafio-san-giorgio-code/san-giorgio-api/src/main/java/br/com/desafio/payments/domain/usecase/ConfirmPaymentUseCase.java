package br.com.desafio.payments.domain.usecase;

import br.com.desafio.payments.domain.model.PaymentModel;

public interface ConfirmPaymentUseCase {
    PaymentModel confirmPayment(PaymentModel paymentModel);
}
