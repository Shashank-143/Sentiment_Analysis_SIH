import Footer from "../components/footer";
import { Navbar } from "../components/navbar";
import SentimentDashboard from "../components/sentiment-dashboard";

export default function Dashboard() {
    return (
        <>
            <Navbar />
            <SentimentDashboard />
            <Footer />
        </>
    );
}
