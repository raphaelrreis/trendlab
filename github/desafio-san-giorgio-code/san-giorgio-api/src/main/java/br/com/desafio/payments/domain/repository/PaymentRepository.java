package br.com.desafio.payments.domain.repository;

import br.com.desafio.payments.domain.model.PaymentModel;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PaymentRepository extends JpaRepository<PaymentModel, Long> {
    List<PaymentModel> findBySellerId(Long sellerId);

    PaymentModel findByBillingCode(String billingCode);

    boolean existsBySellerIdAndBillingCode(Long sellerId, String billingCode);

    PaymentModel save(PaymentModel paymentModel);

}
