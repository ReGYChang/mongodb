package org.omni.mongo;

import com.mongodb.*;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;


public class Main {
    public static void main(String[] args){
        try{
            System.setProperty("javax.net.ssl.trustStore","mongo-java-driver/src/main/resources/tls/ca-cert");
            System.setProperty("javax.net.ssl.trustStorePassword","storepass");
            System.setProperty("javax.net.ssl.keyStore","mongo-java-driver/src/main/resources/tls/keystore");
            System.setProperty("javax.net.ssl.keyStorePassword","storepass");

            ConnectionString connectionString = new ConnectionString("mongodb://admin:admin@hostname/?authSource=admin");

            SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            KeyStore ks = KeyStore.getInstance("JKS");
            KeyStore tks = KeyStore.getInstance("JKS");
            ks.load(new FileInputStream("C:\\Users\\71414\\GitHub\\mongodb-examples\\mongo-java-driver\\src\\main\\resources\\tls\\keystore"), 
                    System.getProperty("javax.net.ssl.keyStorePassword").toCharArray());
            tks.load(new FileInputStream("C:\\Users\\71414\\GitHub\\mongodb-examples\\mongo-java-driver\\src\\main\\resources\\tls\\ca-cert"),
                    System.getProperty("javax.net.ssl.trustStorePassword").toCharArray());

            kmf.init(ks, System.getProperty("javax.net.ssl.keyStorePassword").toCharArray());
            tmf.init(tks);

            sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

//            sslContext.init(null,null,null);
            MongoClientSettings settings = MongoClientSettings.builder()
                .applyToSslSettings(builder -> {
                    builder.enabled(true);
                    builder.context(sslContext);
                    builder.invalidHostNameAllowed(true);
                })
                .applyConnectionString(connectionString)
                .build();

            MongoClient mongoClient = MongoClients.create(settings);

            List<Document> databases = mongoClient.listDatabases().into(new ArrayList<>());
            databases.forEach(db -> System.out.println(db.toJson()));

        }catch (Exception e){
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
        }


    }
}
