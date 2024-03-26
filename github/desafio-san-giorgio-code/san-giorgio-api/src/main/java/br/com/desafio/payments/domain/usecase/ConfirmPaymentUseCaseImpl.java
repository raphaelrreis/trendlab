package br.com.desafio.payments.domain.usecase;

import br.com.desafio.payments.domain.model.PaymentModel;
import br.com.desafio.payments.domain.repository.PaymentRepository;
import br.com.desafio.payments.domain.service.SqsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Service
public class ConfirmPaymentUseCaseImpl implements ConfirmPaymentUseCase {

    private final PaymentRepository paymentRepository;
    private final SqsService sqsService;

    @Value("${cloud.aws.sqs.queue.partial-payments}")
    private String partialPaymentsQueueUrl;

    public ConfirmPaymentUseCaseImpl(PaymentRepository paymentRepository, SqsService sqsService) {
        this.paymentRepository = paymentRepository;
        this.sqsService = sqsService;
    }

    @Transactional
    public PaymentModel confirmPayment(PaymentModel paymentModel) {
        boolean paymentExists = paymentRepository.existsBySellerIdAndBillingCode(paymentModel.getSellerId(),
                paymentModel.getBillingCode());

        return paymentExists ?
                paymentRepository.findByBillingCode(paymentModel.getBillingCode()).getStatus().equals("CONFIRMED") ?
                        paymentRepository.findByBillingCode(paymentModel.getBillingCode()) :
                        updateAndReturnConfirmedPayment(paymentModel) :
                createAndReturnNewPayment(paymentModel);
    }

    private PaymentModel updateAndReturnConfirmedPayment(PaymentModel paymentModel) {
        paymentModel.setStatus("CONFIRMED");
        paymentModel.getItems()
                .forEach(item -> item.setPaymentStatus(item.getPaymentValue().compareTo(BigDecimal.ZERO) > 0 ?
                        "CONFIRMED" :
                        "AGUARDANDO_COMPLEMENTO"));

        PaymentModel confirmedPayment = paymentRepository.save(paymentModel);
        sendMessageToQueue(partialPaymentsQueueUrl, "Detalhes do pagamento confirmado: " + confirmedPayment.getId());
        return confirmedPayment;
    }

    private PaymentModel createAndReturnNewPayment(PaymentModel paymentModel) {
        paymentModel.setStatus("CONFIRMED");
        paymentModel.getItems()
                .forEach(item -> item.setPaymentStatus(item.getPaymentValue().compareTo(BigDecimal.ZERO) > 0 ?
                        "CONFIRMED" :
                        "AGUARDANDO_COMPLEMENTO"));

        PaymentModel newPayment = paymentRepository.save(paymentModel);
        sendMessageToQueue(partialPaymentsQueueUrl, "Detalhes do novo pagamento confirmado: " + newPayment.getId());
        return newPayment;
    }


    private void sendMessageToQueue(String queueUrl, String messageBody) {
        sqsService.sendPaymentMessage(queueUrl, messageBody);
    }
}
