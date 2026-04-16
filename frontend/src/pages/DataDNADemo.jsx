import React from 'react';

const DataDNADemo = () => {
  return (
    <div className="bg-surface text-on-surface font-body selection:bg-primary-fixed selection:text-on-primary-fixed light min-h-screen">
      {/* TopAppBar */}
      <nav className="fixed top-0 w-full z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl">
        <div className="flex justify-between items-center max-w-7xl mx-auto px-8 h-20 w-full">
          <div className="text-xl font-bold tracking-tighter text-slate-900 dark:text-white font-['Inter']">
            DataDNA AI
          </div>
          <div className="hidden md:flex items-center gap-10">
            <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Product</a>
            <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Technology</a>
            <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Security</a>
            <a className="text-blue-600 dark:text-blue-400 font-bold font-['Inter'] tracking-tight" href="#">Demo</a>
          </div>
          <button className="bg-gradient-to-r from-primary to-primary-container text-on-primary px-6 py-2.5 rounded-xl font-semibold hover:opacity-80 transition-all">
            Get Started
          </button>
        </div>
      </nav>

      <main className="pt-32 pb-24 px-6 md:px-12 max-w-7xl mx-auto">
        {/* Hero Section */}
        <div className="mb-20 text-center md:text-left max-w-3xl">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter text-on-surface mb-6 leading-[1.1]">
            Genomic Verification <br/> <span className="text-primary">In Real-Time.</span>
          </h1>
          <p className="text-xl text-on-surface-variant leading-relaxed font-light">
            Experience the precision of our neural fingerprinting engine. Securely upload sequence data to identify provenance and integrity with unparalleled accuracy.
          </p>
        </div>

        {/* Demo Interface (Asymmetric Bento Grid) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Upload Zone */}
          <div className="lg:col-span-7 bg-surface-container-low rounded-[2rem] p-8 md:p-12 relative overflow-hidden group">
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-8">
                <div className="micro-pulse w-2 h-2"></div>
                <span className="text-sm font-bold tracking-widest text-primary uppercase">Neural Input Engine</span>
              </div>
              
              {/* Drag and Drop Canvas */}
              <div className="aspect-[4/3] w-full bg-surface-container-lowest rounded-3xl border border-dashed border-outline-variant/30 flex flex-col items-center justify-center p-12 transition-all hover:bg-white hover:shadow-2xl hover:shadow-primary/5 group-hover:scale-[1.01]">
                <span className="material-symbols-outlined text-6xl text-primary/40 mb-6 group-hover:text-primary transition-colors">genetics</span>
                <h3 className="text-2xl font-bold tracking-tight mb-2 text-on-surface">Drag &amp; Drop Sequence Data</h3>
                <p className="text-on-surface-variant text-center mb-8 max-w-sm">Support for FASTQ, BAM, or CRAM encrypted files. Secure end-to-end processing.</p>
                <div className="flex flex-col sm:flex-row gap-4 w-full max-w-xs">
                  <button className="flex-1 bg-primary text-on-primary px-8 py-4 rounded-xl font-bold text-center hover:opacity-90 transition-all flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined">upload</span>
                    Upload
                  </button>
                  <button className="flex-1 bg-surface-container-high text-on-surface px-8 py-4 rounded-xl font-bold text-center hover:bg-surface-container-highest transition-all flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined">search_check</span>
                    Detect
                  </button>
                </div>
              </div>
            </div>
            {/* Abstract Background Visual */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 blur-[120px] rounded-full translate-x-1/2 -translate-y-1/2"></div>
          </div>

          {/* Analysis Sidebar */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            {/* Status Card */}
            <div className="bg-surface-container-lowest rounded-[2rem] p-8 shadow-sm">
              <div className="flex justify-between items-center mb-8">
                <h4 className="text-lg font-bold tracking-tight">Analysis Pulse</h4>
                <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">Active</span>
              </div>
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-2xl">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined">fingerprint</span>
                    </div>
                    <div>
                      <p className="text-xs text-on-surface-variant font-medium">Detection Result</p>
                      <p className="text-lg font-bold">Biotech Corp Alpha</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-on-surface-variant font-medium">Confidence</p>
                    <p className="text-lg font-bold text-primary">99.98%</p>
                  </div>
                </div>
                {/* Progress Bar Container */}
                <div className="bg-surface-container-low p-6 rounded-2xl">
                  <div className="flex justify-between mb-4">
                    <span className="text-sm font-bold">Matching Provenance...</span>
                    <span className="text-sm font-bold text-primary italic">Scanning</span>
                  </div>
                  <div className="w-full bg-surface-container-highest h-2 rounded-full overflow-hidden">
                    <div className="h-full bg-primary w-[74%] rounded-full shadow-[0_0_8px_rgba(0,78,159,0.5)]"></div>
                  </div>
                  <div className="mt-4 grid grid-cols-3 gap-2">
                    <div className="h-1 bg-primary/20 rounded-full"></div>
                    <div className="h-1 bg-primary/20 rounded-full"></div>
                    <div className="h-1 bg-surface-container-highest rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Secondary Insight Card */}
            <div className="bg-primary text-on-primary rounded-[2rem] p-8 relative overflow-hidden">
              <div className="relative z-10">
                <h4 className="text-xl font-bold mb-4 tracking-tight">Enterprise Security</h4>
                <p className="text-on-primary-container text-sm leading-relaxed mb-6 opacity-80">
                  Your data is processed in a transient, hardware-encrypted enclave. No permanent storage is used during the demo scan.
                </p>
                <a className="text-sm font-bold underline underline-offset-4 hover:opacity-80 transition-opacity" href="#">Read Security Whitepaper</a>
              </div>
              <span className="material-symbols-outlined absolute -bottom-4 -right-4 text-9xl opacity-10 pointer-events-none">verified_user</span>
            </div>

            {/* Visual Element */}
            <div className="h-48 rounded-[2rem] overflow-hidden">
              <img alt="Scientific data visualization" className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDt_EJqpOIaPPStPt3kJ_n0oRaLst7c5gz1PHc7lm_zsKQO0kEHBjUIqxY4siU-FmfVHPO1VMjFNnalOAoMbRVbAp0Y8A4fcMb1BK9iQ71sOk9B_jwWCvZYulCecsZf3EBxDAkTsScLKiZ4ho2aQ7UQlti1QL0gwe8-xPaY7CXe-TBxePfNumdEiDPE1FvYY_G1IVv5vrFSPWUmQ0ZObm_cSjSuXaJQ27xkKJ80ixxBVkXtYRm8FFoURFu6mjYEyMCE62wnWDMr5RMR"/>
            </div>
          </div>
        </div>

        {/* Technology Features (Asymmetric) */}
        <section className="mt-32">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-8">
            <div className="max-w-xl">
              <h2 className="text-4xl font-extrabold tracking-tighter mb-4 leading-tight">Under the Hood of <br/>Precision AI.</h2>
              <p className="text-on-surface-variant">Our engine combines transformer models with cryptographic hashing to ensure that genomic fingerprints are both unique and privacy-preserving.</p>
            </div>
            <div className="pb-1">
              <button className="bg-surface-container-high text-on-surface px-8 py-4 rounded-full font-bold hover:bg-surface-container-highest transition-all flex items-center gap-2">
                Technical Architecture
                <span className="material-symbols-outlined">arrow_forward</span>
              </button>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-10 rounded-[2rem] bg-surface-container-low transition-all hover:bg-surface-container-highest">
              <span className="material-symbols-outlined text-primary text-4xl mb-6">shutter_speed</span>
              <h5 className="text-xl font-bold mb-4">Sub-Second Latency</h5>
              <p className="text-sm text-on-surface-variant leading-relaxed">Proprietary indexing allows for near-instant identification across petabyte-scale genetic databases.</p>
            </div>
            <div className="p-10 rounded-[2rem] bg-surface-container-low transition-all hover:bg-surface-container-highest">
              <span className="material-symbols-outlined text-primary text-4xl mb-6">encrypted</span>
              <h5 className="text-xl font-bold mb-4">Zero-Knowledge Proofs</h5>
              <p className="text-sm text-on-surface-variant leading-relaxed">Verify genetic provenance without ever exposing the sensitive underlying sequence data.</p>
            </div>
            <div className="p-10 rounded-[2rem] bg-surface-container-low transition-all hover:bg-surface-container-highest">
              <span className="material-symbols-outlined text-primary text-4xl mb-6">hub</span>
              <h5 className="text-xl font-bold mb-4">Global Ledger</h5>
              <p className="text-sm text-on-surface-variant leading-relaxed">Immutable tracking of genetic intellectual property across jurisdictional borders.</p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-8 py-16 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex flex-col gap-2 items-center md:items-start">
            <div className="text-lg font-bold text-slate-900 dark:text-white font-['Inter']">DataDNA AI</div>
            <p className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400">© 2024 DataDNA AI. Precision Genomic Fingerprinting.</p>
          </div>
          <div className="flex gap-8 flex-wrap justify-center">
            <a className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" href="#">Privacy Policy</a>
            <a className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" href="#">Terms of Service</a>
            <a className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" href="#">API Documentation</a>
            <a className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" href="#">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default DataDNADemo;
