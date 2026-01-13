import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'FlowTask - AI-Powered Productivity Platform',
  description: 'Streamline your workflow with our intelligent task management solution',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans bg-background text-text-primary">
        <div className="min-h-screen bg-background">
          {children}
        </div>
      </body>
    </html>
  );
}