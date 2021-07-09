package org.omni.mongo;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import java.text.SimpleDateFormat;
import java.util.Date;


public class Main {
    public static void main(String[] args){
        try{
            MongoClientURI uri = new MongoClientURI("mongodb://admin:admin@35.229.235.134:27020/?authSource=admin");
            MongoClient client = new MongoClient(uri);
            MongoDatabase test = client.getDatabase("test");
            MongoCollection<Document> ha_test = test.getCollection("ha_test");

            SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

            System.out.println("Connect to database successfully!");
            System.out.println("MongoDatabase info is : "+test.getName());

            for (int i = 100475; i <= 150000; i++){
                Date date = new Date();
                MongoCollection coll = test.getCollection("ha_test");
                Document doc = new Document("name", "HA")
                        .append("ns", i)
                        .append("ts", date);
                ha_test.insertOne(doc);
            }
        }catch (Exception e){
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
        }


    }
}
