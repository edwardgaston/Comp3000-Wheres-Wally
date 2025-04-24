// filepath: d:\Coding Projects\Comp3000-Wheres-Wally\website\backend\src\config\db.js
import mongoose from "mongoose";
import colors from "colors";

colors.enable(); // Enable colors for string formatting

const connectDB = async () => {
    try {
        const conn = await mongoose.connect(process.env.MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log(`MongoDB Connected: ${conn.connection.host}`.cyan.underline);
    } catch (error) {
        console.error(`Error: ${error.message}`.red.underline.bold);
        process.exit(1); // Exit process with failure
    }
};

export default connectDB;