from minio import Minio
from dataclasses import dataclass
from configparser import ConfigParser
import logging
from typing import List, Optional, Dict


@dataclass
class MinioClient:
    filename: str = 'config.ini'
    
    def __post_init__(self) -> None:
        """Initialize Minio client and configure logging"""
        self._setup_config()
        self._setup_logging()
        self._initialize_minio_client()
        self.logger.info("MinioClient initialized")
    
    def _setup_config(self) -> None:
        """Read configuration from INI file."""
        self.cfg = ConfigParser()
        self.cfg.read(self.filename)
        
        self.server = self.cfg.get('minio', 'server')
        self.access_key = self.cfg.get('minio', 'access_key')
        self.secret_key = self.cfg.get('minio', 'secret_key')
        self.log_file = self.cfg.get('minio', 'log_file')
    
    def _setup_logging(self) -> None:
        """Configure logging system."""
        self.logger  = logging.getLogger(self.log_file)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(file_handler)

    def _initialize_minio_client(self) -> None:
        """Initialize Minio client instance."""
        self.client = Minio(
            endpoint=self.server,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )

    def bucket_exists(self, bucket_name: str) -> bool:
        """Check if bucket exists."""
        try:
            return self.client.bucket_exists(bucket_name)
        except Exception as e:
            self.logger.error(f"Error checking bucket {bucket_name}: {str(e)}")
            return False
    
    def create_bucket(self, bucket_name: str) -> bool:
        """Create a new bucket."""
        try:
            if not self.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                self.logger.info(f"Bucket created: {bucket_name}")
                return True
            self.logger.warning(f"Bucket already exists: {bucket_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error creating bucket {bucket_name}: {str(e)}")
            return False
    
    def remove_bucket(self, bucket_name: str) -> bool:
        """Remove a bucket."""
        try:
            if self.bucket_exists(bucket_name):
                self.client.remove_bucket(bucket_name)
                self.logger.info(f"Bucket removed: {bucket_name}")
                return True
            self.logger.warning(f"Bucket not found: {bucket_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error removing bucket {bucket_name}: {str(e)}")
            return False
    
    def list_buckets(self) -> List[str]:
        """List all available buckets."""
        try:
            return [bucket.name for bucket in self.client.list_buckets()]
        except Exception as e:
            self.logger.error(f"Error listing buckets: {str(e)}")
            return []

    # Object operations
    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        """Check if object exists in bucket."""
        try:
            self.client.stat_object(bucket_name, object_name)
            return True
        except Exception as e:
            self.logger.debug(f"Object not found {bucket_name}/{object_name}: {str(e)}")
            return False
    
    def list_objects(self, bucket_name: str, prefix: str = '', recursive: bool = True) -> List[str]:
        """List all objects in the bucket."""
        try:
            objects = self.client.list_objects(
                bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            return [obj.object_name for obj in objects]
        except Exception as e:
            self.logger.error(f"Error listing objects in {bucket_name}: {str(e)}")
            return []
    
    def get_object_url(self, bucket_name: str, object_name: str) -> Optional[str]:
        """Generate presigned URL for object access."""
        try:
            if self.object_exists(bucket_name, object_name):
                return self.client.presigned_get_object(
                    bucket_name,
                    object_name
                )
            return None
        except Exception as e:
            self.logger.error(f"Error generating URL for {bucket_name}/{object_name}: {str(e)}")
            return None
    
    def get_file(self, bucket_name: str, object_name: str) -> Optional[bytes]:
        """Get file content from Minio."""
        try:
            if self.object_exists(bucket_name, object_name):
                response = self.client.get_object(bucket_name, object_name)
                data = response.data
                response.close()
                response.release_conn()
                return data
            return None
        except Exception as e:
            self.logger.error(f"Error getting object {bucket_name}/{object_name}: {str(e)}")
            return None

    def put_file(
        self,
        bucket_name: str,
        object_name: str,
        file_path: str,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
        overwrite: bool = False
    ) -> bool:
        """
        Upload file to Minio with custom metadata. Creates bucket if it doesn't exist.
        
        Args:
            bucket_name: Name of the bucket (will be created if doesn't exist)
            object_name: Name of the object to create
            file_path: Path to local file to upload
            content_type: MIME type of the file
            metadata: Custom metadata dictionary (key-value pairs)
            overwrite: Whether to overwrite existing file
            
        Returns:
            bool: True if upload succeeded, False otherwise
        """
        try:
            # Check if bucket exists, create if not
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                self.logger.info(f"Created bucket: {bucket_name}")
            
            # Check if object exists (if overwrite is False)
            if not overwrite and self.object_exists(bucket_name, object_name):
                self.logger.warning(f"Object already exists: {bucket_name}/{object_name}")
                return False
            
            # Prepare metadata with content type
            headers = metadata or {}
            headers["Content-Type"] = content_type
            
            # Upload the file
            self.client.fput_object(
                bucket_name,
                object_name,
                file_path,
                metadata=headers
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Error uploading {bucket_name}/{object_name}: {str(e)}")
            return False
    
    def remove_file(self, bucket_name: str, object_name: str) -> bool:
        """Remove file from Minio."""
        try:
            if self.object_exists(bucket_name, object_name):
                self.client.remove_object(bucket_name, object_name)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error removing {bucket_name}/{object_name}: {str(e)}")
            return False
    
    def get_object_metadata(self, bucket_name: str, object_name: str) -> Optional[Dict]:
        """Get metadata for an object."""
        try:
            if self.object_exists(bucket_name, object_name):
                obj = self.client.stat_object(bucket_name, object_name)
                return obj

            return None
        except Exception as e:
            self.logger.error(f"Error getting metadata for {bucket_name}/{object_name}: {str(e)}")
            return None
