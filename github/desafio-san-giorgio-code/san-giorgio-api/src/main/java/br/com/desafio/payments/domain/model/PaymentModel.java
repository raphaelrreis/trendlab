package br.com.desafio.payments.domain.model;

import br.com.desafio.payments.dto.PaymentItemDTO;
import lombok.*;

import javax.persistence.*;
import java.util.List;

@Entity
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class PaymentModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long sellerId;
    private String billingCode;
    private String status;

    @OneToMany(mappedBy = "paymentModel", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<PaymentItemDTO> items;
}
