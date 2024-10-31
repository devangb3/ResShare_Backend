// app.js
import express from 'express';
import fileRoutes from './routes/fileRoutes.js';

const app = express();
app.use(express.json());

// Routes
app.use('/files', fileRoutes);

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
