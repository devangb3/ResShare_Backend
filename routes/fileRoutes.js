import express from 'express';
import multer from 'multer';
import crypto from 'crypto';
import { create } from 'ipfs-http-client';
import axios from 'axios';

const router = express.Router();
const upload = multer();
const ipfs = create({ host: 'localhost', port: '5001', protocol: 'http' });

const GRAPHQL_URL =
 "https://cloud.resilientdb.com/graphql";
//'http://127.0.0.1:8000/graphql';

const YOUR_SIGNER_PUBLIC_KEY = "jdA6PXTp3mBWNpJrtan78UVrfo1PThPv8ykGwmSqXbH";  //update your_signer_public_key
const RECIPIENT_PUBLIC_KEY = "3H2eTSTiAdVnj7rXV8LKyrhYGXSH38kn8ucuno7pyfaw";  //update recipient_public_key
const YOUR_PRIVATE_KEY = "5kTmRsESRYf8qkKAmrmzwzaRiPCk2CEwA4RzvZXKt9jd";  //update your_private_key

// GraphQL request function
async function graphqlRequest(query, variables) {
    try {
        const response = await axios.post(GRAPHQL_URL, {
            query,
            variables,
        });
        return response.data.data;
    } catch (error) {
        console.error('GraphQL request error:', error);
        throw new Error('Failed to communicate with ResilientDB');
    }
}

// Encryption utility
function encrypt(buffer, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    const encryptedData = Buffer.concat([iv, cipher.update(buffer), cipher.final()]);
    return encryptedData;
}

// Decryption utility
function decrypt(encryptedBuffer, key) {
    const iv = encryptedBuffer.slice(0, 16); 
    const encryptedData = encryptedBuffer.slice(16);
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    const decrypted = Buffer.concat([decipher.update(encryptedData), decipher.final()]);
    return decrypted;
}

// Key generation
function generateKey() {
    return crypto.randomBytes(32); // AES-256 requires 32 bytes
}

// Normalize encryption key to 32 bytes
function normalizeKey(encryptionKey) {
    const keyBuffer = Buffer.from(encryptionKey, 'hex');
    if (keyBuffer.length < 32) {
        const paddedKey = Buffer.alloc(32);
        keyBuffer.copy(paddedKey);
        return paddedKey;
    } else if (keyBuffer.length > 32) {
        return keyBuffer.slice(0, 32);
    }
    return keyBuffer;
}

// Upload route
router.post('/upload', upload.single('file'), async (req, res) => {
    try {
        const { filename } = req.body;

        if (!req.file || !filename) {
            return res.status(400).json({ message: 'Missing file or filename in request' });
        }

        const fileBuffer = req.file.buffer;
        const fileHash = crypto.createHash('sha256').update(fileBuffer).digest('hex');
        const encryptionKey = generateKey();
        const keyBuffer = normalizeKey(encryptionKey.toString('hex'));

        const encryptedData = encrypt(fileBuffer, keyBuffer);
        const ipfsResult = await ipfs.add(encryptedData);
        const ipfsHash = ipfsResult.path;

        // const query = `
        //     mutation ($filename: String!, $ipfsHash: String!, $fileHash: String!, $encryptionKey: String!) {
        //         addFile(filename: $filename, ipfsHash: $ipfsHash, fileHash: $fileHash, encryptionKey: $encryptionKey) {
        //             id
        //         }
        //     }
        // `;
        // const variables = { filename, ipfsHash, fileHash, encryptionKey: encryptionKey.toString('hex') };
        
        //HERE START
        // GraphQL mutation variables for postTransaction
        const query = `
            mutation ($operation: String!, $amount: Int!, $signerPublicKey: String!, $signerPrivateKey: String!, $recipientPublicKey: String!, $asset: String!) {
                postTransaction(
                    data: {
                        operation: $operation,
                        amount: $amount,
                        signerPublicKey: $signerPublicKey,
                        signerPrivateKey: $signerPrivateKey,
                        recipientPublicKey: $recipientPublicKey,
                        asset: $asset
                    }
                ){id}
            }
        `;

        // const assetData = JSON.stringify({
        //     filename,
        //     ipfsHash: ipfsHash,
        //     fileHash,
        //     encryptionKey
        // });

        const assetData = JSON.stringify({
            data: {
                filename,
                ipfsHash: ipfsHash,
                fileHash,
                encryptionKey
            }
        });

        const variables = {
            operation: "CREATE",
            amount: 10,
            signerPublicKey: YOUR_SIGNER_PUBLIC_KEY, //'<YOUR_SIGNER_PUBLIC_KEY>',
            signerPrivateKey: YOUR_PRIVATE_KEY, //'<YOUR_SIGNER_PRIVATE_KEY>',
            recipientPublicKey: RECIPIENT_PUBLIC_KEY, //'<RECIPIENT_PUBLIC_KEY>',
            asset: assetData
        };
        //HERE ENDS
        
        const result = await graphqlRequest(query, variables);
        
        //console.log("File uploaded with ID:", result.addFile.id);
        console.log("File uploaded with ID:", result.postTransaction.id);


        res.status(200).json({ message: 'File uploaded successfully', fileId: result.postTransaction.id});
    } catch (error) {
        console.error('Error uploading file:', error);
        res.status(500).json({ message: 'File upload failed' });
    }
});

// Download route
router.get('/download/:id', async (req, res) => {
    try {
        // const query = `
        //     query ($id: ID!) {
        //         getFile(id: $id) {
        //             id
        //             filename
        //             ipfsHash
        //             fileHash
        //             encryptionKey
        //         }
        //     }
        // `;

        const query = `
            query ($id: ID!) {
                getTransaction(id: $id) {
                    asset
                }
            }
        `;

        const variables = { id: req.params.id };
        const result = await graphqlRequest(query, variables);
        //const fileRecord = result.getFile;
        const fileRecord = result.getTransaction;


        if (!fileRecord) {
            return res.status(404).json({ message: 'File not found' });
        }

        const { asset } = result.getTransaction;
        //console.log(asset)
        const jsonString = asset
            .replace(/'/g, '"')                      // Replace single quotes with double quotes
            .replace(/"Buffer"/g, '"Buffer"')        // Make sure Buffer type is in double quotes
            .replace(/"data":\s+\[/g, '"data": [');  // Ensure proper format for the array
        const parsedData = JSON.parse(jsonString);
        const { filename, ipfsHash, fileHash, encryptionKey } = parsedData.data   
        //console.log(filename, ipfsHash, fileHash, encryptionKey)
        
        // const ipfsFileChunks = [];
        // for await (const chunk of ipfs.cat(fileRecord.ipfsHash)) {
        //     ipfsFileChunks.push(chunk);
        // }
        // const encryptedBuffer = Buffer.concat(ipfsFileChunks);

        // const key = normalizeKey(fileRecord.encryptionKey);
        // const decryptedFile = decrypt(encryptedBuffer, key);

        // const retrievedFileHash = crypto.createHash('sha256').update(decryptedFile).digest('hex');
        //console.log(`Retrieved File Hash: ${retrievedFileHash}`);
        //console.log(`Stored File Hash: ${fileRecord.fileHash}`);
        
        // if (retrievedFileHash !== fileRecord.fileHash) {
        //     return res.status(400).json({ message: 'File integrity check failed' });
        // }

        // res.status(200).json({
        //     filename: fileRecord.filename,
        //     fileContent: decryptedFile.toString('base64')
        // });

         const ipfsFileChunks = [];
         for await (const chunk of ipfs.cat(ipfsHash)) {
            ipfsFileChunks.push(chunk);
        }
        
        const encryptedBuffer = Buffer.concat(ipfsFileChunks);
        const key = normalizeKey(encryptionKey);
        const decryptedFile = decrypt(encryptedBuffer, key);
 
         // Verify integrity by checking hash
         const retrievedFileHash = crypto.createHash('sha256').update(decryptedFile).digest('hex');
         if (retrievedFileHash !== fileHash) {
             return res.status(400).json({ message: 'File integrity check failed' });
         }

        // Send the file as a download to the user's download folder
        res.setHeader('Content-Disposition', `attachment; filename="${filename}"`); // Set content disposition for download
        res.setHeader('Content-Type', 'application/octet-stream'); // Set content type
        res.send(decryptedFile); // Send the decrypted file directly

        // res.status(200).json({
        //     filename: filename,
        //     fileContent: decryptedFile.toString('base64')
        //  });

    } catch (error) {
        console.error('Error downloading file:', error);
        res.status(500).json({ message: 'File download failed' });
    }
});

export default router;
