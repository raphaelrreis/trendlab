package br.com.desafio.payments.controller;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.service.PaymentService;
import br.com.desafio.payments.domain.usecase.ConfirmPaymentUseCase;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/payments")
public class PaymentController {

    private final ConfirmPaymentUseCase confirmPaymentUseCase;
    private final PaymentService paymentService;

    @Autowired
    public PaymentController(ConfirmPaymentUseCase confirmPaymentUseCase, PaymentService paymentService) {
        this.confirmPaymentUseCase = confirmPaymentUseCase;
        this.paymentService = paymentService;
    }

    @PutMapping("/confirm")
    public ResponseEntity<PaymentModel> confirmPayment(@RequestBody PaymentModel paymentModel) {
        PaymentModel confirmedPayment = confirmPaymentUseCase.confirmPayment(paymentModel);
        return ResponseEntity.ok(confirmedPayment);
    }

    @GetMapping("/seller/{sellerId}")
    public ResponseEntity<List<PaymentModel>> getPaymentsBySellerId(@PathVariable Long sellerId) {
        List<PaymentModel> payments = paymentService.getPaymentsBySellerId(sellerId);
        return ResponseEntity.ok(payments);
    }

    @GetMapping("/billingCode/{billingCode}")
    public ResponseEntity<PaymentModel> getPaymentByBillingCode(@PathVariable String billingCode) {
        PaymentModel payment = paymentService.getPaymentByBillingCode(billingCode);
        return ResponseEntity.ok(payment);
    }

    @GetMapping("/validate/{sellerId}/{billingCode}")
    public ResponseEntity<Boolean> validatePaymentExists(@PathVariable Long sellerId,
                                                         @PathVariable String billingCode) {
        boolean exists = paymentService.validatePaymentExists(sellerId, billingCode);
        return ResponseEntity.ok(exists);
    }

    @PutMapping("/save")
    public ResponseEntity<PaymentModel> savePayment(@RequestBody PaymentModel paymentModel) {
        PaymentModel savedPayment = paymentService.savePayment(paymentModel);
        return ResponseEntity.ok(savedPayment);
    }
}
