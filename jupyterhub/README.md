# JupyterHub 
### Building the Docker Image
See Dockerfile.

### Example Spark
See or upload `Untilted.ipynb`.

```
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
```

``` 
sparkConf = SparkConf()
sparkConf.setMaster("k8s://https://kubernetes.default.svc.cluster.local:443")
sparkConf.setAppName("test-spark-app")
sparkConf.set("spark.kubernetes.container.image", "wbassler/pyspark-aws:3.1.2")
sparkConf.set("spark.kubernetes.namespace", "spark")
sparkConf.set("spark.executor.instances", "1")
sparkConf.set("spark.executor.cores", "1")
# Testing memory is used to override the min of what the actual needs
sparkConf.set("spark.testing.memory", "2147480000")
sparkConf.set("spark.executor.memory", "1g")
sparkConf.set("spark.kubernetes.pyspark.pythonVersion", "3")
sparkConf.set("spark.kubernetes.authenticate.driver.serviceAccountName", "spark")
sparkConf.set("spark.kubernetes.authenticate.serviceAccountName", "spark")
sparkConf.set("spark.driver.port", "2222")
sparkConf.set("spark.driver.host", "driver-service.jupyterhub.svc.cluster.local")
sparkConf.set("spark.driver.bindAddress", "0.0.0.0")
sparkConf.set("spark.eventLog.dir", "s3a://spark-history/logs/")
sparkConf.set("spark.eventLog.enabled", True)
###### S3 Information for Minio
sparkConf.set("spark.hadoop.fs.s3a.access.key", "minio")
sparkConf.set("spark.hadoop.fs.s3a.secret.key", "minio123")
sparkConf.set("spark.hadoop.fs.s3a.endpoint", "mlflow-minio-service.mlflow.svc.cluster.local:9000")
sparkConf.set("spark.hadoop.fs.s3a.path.style.access", True)
sparkConf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", False)
sparkConf.set("spark.hadoop.com.amazonaws.services.s3.enableV4", True)
sparkConf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

###### Ignite the Worker Nodes
spark = SparkSession.builder.config(conf=sparkConf).getOrCreate()
sc = spark.sparkContext
```

``` 
# Example Spark App
from random import random
from operator import add
partitions = 7
n = 10000000 * partitions

def f(_):
    x = random() * 2 - 1
    y = random() * 2 - 1
    
    return 1 if x ** 2 + y ** 2 <= 1 else 0

count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
```

``` 
print("Pi is roughly %f" % (4.0 * count / n))
```

``` 
# Stop the workers
sc.stop()
```