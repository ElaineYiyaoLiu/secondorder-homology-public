import type { Metadata } from 'next';
import './globals.css';
export const metadata:Metadata={title:'SecondOrder Homology',description:'A persistent homology research workspace for testing whether market structure adds out-of-sample information.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
