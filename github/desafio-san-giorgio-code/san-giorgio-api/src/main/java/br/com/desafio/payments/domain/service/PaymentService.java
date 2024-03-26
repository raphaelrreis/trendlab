package br.com.desafio.payments.domain.service;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.repository.PaymentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PaymentService {

    private final PaymentRepository paymentRepository;

    @Autowired
    public PaymentService(PaymentRepository paymentRepository) {
        this.paymentRepository = paymentRepository;
    }

    public PaymentModel getPaymentByBillingCode(String billingCode) {
        return paymentRepository.findByBillingCode(billingCode);
    }

    public List<PaymentModel> getPaymentsBySellerId(Long sellerId) {
        return paymentRepository.findBySellerId(sellerId);
    }

    public boolean validatePaymentExists(Long sellerId, String billingCode) {
        return paymentRepository.existsBySellerIdAndBillingCode(sellerId, billingCode);
    }

    public PaymentModel savePayment(PaymentModel paymentModel) {
        return paymentRepository.save(paymentModel);
    }
}
