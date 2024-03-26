package br.com.desafio.payments.domain.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

@Service
public class SqsService {

    private SqsClient sqsClient;

    private static final Logger logger = LoggerFactory.getLogger(SqsService.class);


    @Autowired
    public SqsService(@Value("${cloud.aws.region}") Region region) {
        this.sqsClient =
                SqsClient.builder().credentialsProvider(DefaultCredentialsProvider.create()).region(region).build();
    }

    public void setSqsClient(SqsClient sqsClient) {
        this.sqsClient = sqsClient;
    }

    public void sendPaymentMessage(String queueUrl, String messageBody) {
        try {
            SendMessageRequest sendMsgRequest =
                    SendMessageRequest.builder().queueUrl(queueUrl).messageBody(messageBody).build();
            sqsClient.sendMessage(sendMsgRequest);
            logger.info("Mensagem enviada para SQS: {}", queueUrl);
        } catch (Exception e) {
            logger.error("Erro ao enviar mensagem para SQS: {}", e.getMessage(), e);
            throw new RuntimeException("Falha ao enviar mensagem para SQS", e);
        }
    }
}
