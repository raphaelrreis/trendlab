package br.com.desafio.payments.domain.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class SqsServiceTest {

    @Mock
    private SqsClient sqsClient;

    private SqsService sqsService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.initMocks(this);
        sqsService = new SqsService(Region.of("us-east-1"));
        sqsService.setSqsClient(sqsClient);
    }

    @Test
    void testSendPaymentMessage() {
        String queueUrl = "URL_DA_FILA_PARCIAL";
        String messageBody = "Test message";

        when(sqsClient.sendMessage(any(SendMessageRequest.class))).thenReturn(null);

        sqsService.sendPaymentMessage(queueUrl, messageBody);

        SendMessageRequest expectedRequest =
                SendMessageRequest.builder().queueUrl(queueUrl).messageBody(messageBody).build();
        verify(sqsClient).sendMessage(expectedRequest);
    }
}
