import React from 'react';

const DataDNALanding = () => {
  return (
    <div className="bg-surface text-on-surface selection:bg-primary-fixed selection:text-on-primary-fixed light min-h-screen">
      {/* TopAppBar */}
      <header className="fixed top-0 w-full z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl">
        <nav className="flex justify-between items-center max-w-7xl mx-auto px-8 h-20 w-full">
          <div className="flex items-center gap-8">
            <a className="text-xl font-bold tracking-tighter text-slate-900 dark:text-white" href="#">DataDNA AI</a>
            <div className="hidden md:flex items-center gap-6">
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Product</a>
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Technology</a>
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Security</a>
              <a className="text-blue-600 dark:text-blue-400 font-bold font-['Inter'] tracking-tight" href="#">Demo</a>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="bg-primary hover:opacity-80 transition-all text-on-primary px-6 py-2.5 rounded-xl font-semibold text-sm">Get Started</button>
          </div>
        </nav>
      </header>

      <main className="pt-20">
        {/* Hero Section */}
        <section className="relative min-h-[921px] flex items-center justify-center overflow-hidden px-8">
          <div className="max-w-5xl mx-auto text-center z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high mb-8">
              <span className="w-2 h-2 rounded-full bg-primary shadow-[0_0_10px_rgba(0,78,159,0.5)]"></span>
              <span className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Genomic Protection 2.0</span>
            </div>
            <h1 className="text-6xl md:text-8xl font-extrabold tracking-tighter text-on-surface mb-8 leading-[0.9]">
              Own Your Data.<br/>Track Every File.
            </h1>
            <p className="text-xl md:text-2xl text-on-surface-variant max-w-2xl mx-auto mb-12 font-medium leading-relaxed">
              Embed immutable digital fingerprints into your datasets. Detect leaks, verify ownership, and protect your AI training assets with surgical precision.
            </p>
            <div className="flex flex-col md:flex-row items-center justify-center gap-6">
              {/* Note: The 'hero-gradient' class uses inline CSS from the original HTML. We add inline style here for completeness. */}
              <button 
                className="text-on-primary px-10 py-5 rounded-xl font-bold text-lg hover:scale-[1.02] transition-transform shadow-xl"
                style={{ background: 'linear-gradient(135deg, #004e9f 0%, #0066cc 100%)' }}
              >
                Try Demo
              </button>
              <button className="bg-surface-container-high text-on-surface px-10 py-5 rounded-xl font-bold text-lg hover:bg-surface-container-highest transition-colors">Watch Film</button>
            </div>
          </div>
          {/* Aesthetic Abstract background element */}
          <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary-fixed/20 rounded-full blur-[120px]"></div>
          <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-200/20 rounded-full blur-[120px]"></div>
        </section>

        {/* Product Showcase (Bento Grid / Apple Style) */}
        <section className="py-32 px-8 bg-surface-container-low">
          <div className="max-w-7xl mx-auto">
            <div className="mb-20">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4">Engineered for Transparency.</h2>
              <p className="text-lg text-on-surface-variant max-w-xl">Four pillars of digital sovereignity, powered by advanced steganographic AI.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
              {/* Card 1 */}
              <div className="md:col-span-8 bg-surface-container-lowest rounded-[2rem] p-10 flex flex-col justify-between overflow-hidden relative group min-h-[450px]">
                <div className="z-10">
                  <span className="material-symbols-outlined text-primary text-4xl mb-6">fingerprint</span>
                  <h3 className="text-3xl font-bold mb-4">Invisible Fingerprinting</h3>
                  <p className="text-on-surface-variant max-w-md text-lg">Inject imperceptible, mathematically unique signatures into any file format without altering data integrity or performance.</p>
                </div>
                <img className="absolute right-0 bottom-0 w-1/2 h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-700" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAfyBLLNJG8fCqtb4V9N-Uz35Ql_HAKwM4PvL384tcXY0cpJpNWQgVH3Ir1eSgfze7hY9EMA_7giWSJB2-QbEpU-0TH8uKyNG4HNWkvKLLZwcwGKoFVkj0sJPgqjSjAAJ9voLFJBwN_rUuxsnPLkKvnAXmaEvHS1cXHnZEiMaDOyZAXv7WiZumWZY2IGIKRwERZyIb4_Lg2Al6Hqvp1YoXomSBiXvIQGLZg0TPBTSSVWAiFREVNW86ZnztvHNsZH6be8zlNxC_plL-O" alt="close-up of digital microscopic data structures glowing with neon blue light in a clean studio setting" />
              </div>
              
              {/* Card 2 */}
              <div className="md:col-span-4 bg-surface-container-lowest rounded-[2rem] p-10 flex flex-col justify-between min-h-[450px]">
                <div>
                  <span className="material-symbols-outlined text-primary text-4xl mb-6">leak_add</span>
                  <h3 className="text-3xl font-bold mb-4">Leak Detection</h3>
                  <p className="text-on-surface-variant text-lg">Trace unauthorized distribution back to the source in seconds with our global data-pollen tracking network.</p>
                </div>
                <div className="h-32 bg-surface-container-low rounded-2xl flex items-center justify-center">
                  <span className="text-primary font-bold animate-pulse">Scanning Network...</span>
                </div>
              </div>
              
              {/* Card 3 */}
              <div className="md:col-span-4 bg-surface-container-lowest rounded-[2rem] p-10 flex flex-col justify-between min-h-[450px]">
                <div>
                  <span className="material-symbols-outlined text-primary text-4xl mb-6">verified_user</span>
                  <h3 className="text-3xl font-bold mb-4">Ownership Verification</h3>
                  <p className="text-on-surface-variant text-lg">Cryptographic proof of origin that stands up in legal audits, securing your intellectual property globally.</p>
                </div>
              </div>
              
              {/* Card 4 */}
              <div className="md:col-span-8 bg-surface-container-lowest rounded-[2rem] p-10 flex flex-col justify-between overflow-hidden relative group min-h-[450px]">
                <div className="z-10">
                  <span className="material-symbols-outlined text-primary text-4xl mb-6">psychology</span>
                  <h3 className="text-3xl font-bold mb-4">AI-based Robustness</h3>
                  <p className="text-on-surface-variant max-w-md text-lg">Our DNA persists through format changes, resizing, compression, and even AI re-generation. Indestructible protection.</p>
                </div>
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent z-0"></div>
                <img className="absolute right-0 bottom-0 w-2/3 h-full object-cover group-hover:scale-110 transition-transform duration-1000 z-0" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDfKV7BeVDbxU-CoUp6b7xkfikPXcDRcX2soReJufxExz-gru4fmlR0X4VYW3Ri9HMTdg0tRExdbq195oDVr4ZRX7fLd2_ltzl2YABkfW7-NDUop7_qP-5klDm60ICEBK8qYDEtquZCT7XJqNwW0WYvHxxOZAFhvg37Xt0dlm-fuP085U7UMJraRxFxQtFq_bIaqx0VRbVyhKv-BbeaxROpJKh8YYaYTgih7A2eeVmIGoxIGZgWYlk4ciKVnvfz7RZAq5PYay6UgJhc" alt="abstract neural network visualization with crystalline structures and soft blue light rays representing data security" />
              </div>
            </div>
          </div>
        </section>

        {/* How It Works (Asymmetric Flow) */}
        <section className="py-32 px-8 bg-surface">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
              <div>
                <h2 className="text-5xl font-extrabold tracking-tighter mb-12">The Cycle of Trust.</h2>
                <div className="space-y-16">
                  <div className="flex gap-8 group">
                    <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center font-bold text-primary group-hover:bg-primary group-hover:text-on-primary transition-colors">1</div>
                    <div>
                      <h4 className="text-2xl font-bold mb-2">Upload &amp; Analyze</h4>
                      <p className="text-on-surface-variant leading-relaxed">Simply upload your high-value datasets or media assets. Our AI analyzes the structural DNA of each file.</p>
                    </div>
                  </div>
                  <div className="flex gap-8 group">
                    <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center font-bold text-primary group-hover:bg-primary group-hover:text-on-primary transition-colors">2</div>
                    <div>
                      <h4 className="text-2xl font-bold mb-2">Fingerprint Injection</h4>
                      <p className="text-on-surface-variant leading-relaxed">An invisible, steganographic layer is woven into the data. It's unique to you and practically impossible to remove.</p>
                    </div>
                  </div>
                  <div className="flex gap-8 group">
                    <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center font-bold text-primary group-hover:bg-primary group-hover:text-on-primary transition-colors">3</div>
                    <div>
                      <h4 className="text-2xl font-bold mb-2">Monitor &amp; Verify</h4>
                      <p className="text-on-surface-variant leading-relaxed">Track your data across the web. If a copy is found, use our verify tool to prove ownership instantly.</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="relative bg-surface-container-high rounded-[3rem] p-4 aspect-square flex items-center justify-center">
                <div className="w-full h-full rounded-[2.5rem] overflow-hidden bg-white shadow-2xl flex flex-col">
                  <div className="p-6 border-b border-surface-container flex items-center justify-between">
                    <div className="flex gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-400"></div>
                      <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                      <div className="w-3 h-3 rounded-full bg-green-400"></div>
                    </div>
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">DNA Verifier v4.0</span>
                  </div>
                  <div className="flex-grow p-12 flex flex-col items-center justify-center text-center">
                    <div className="w-24 h-24 rounded-full bg-primary-fixed flex items-center justify-center mb-6">
                      <span className="material-symbols-outlined text-primary text-5xl" style={{fontVariationSettings: "'FILL' 1"}}>check_circle</span>
                    </div>
                    <h5 className="text-3xl font-bold mb-2">100% Match Found</h5>
                    <p className="text-on-surface-variant mb-8">Asset: Training_Dataset_Alpha.csv<br/>Owner: DataDNA Enterprise Admin</p>
                    <button className="bg-primary text-on-primary px-8 py-3 rounded-xl font-bold text-sm">Download Legal Proof</button>
                  </div>
                </div>
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-blue-100 rounded-full -z-10 blur-2xl opacity-50"></div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-32 px-8">
          <div className="max-w-7xl mx-auto">
            <div 
              className="rounded-[3rem] p-16 text-center text-on-primary relative overflow-hidden"
              style={{ background: 'linear-gradient(135deg, #004e9f 0%, #0066cc 100%)' }}
            >
              <h2 className="text-5xl md:text-6xl font-extrabold tracking-tighter mb-8 relative z-10">Secure Your Digital Assets Today.</h2>
              <p className="text-xl md:text-2xl text-on-primary-container max-w-2xl mx-auto mb-12 font-medium relative z-10">
                Join 200+ enterprise teams protecting their intellectual property with the world's most advanced fingerprinting technology.
              </p>
              <div className="relative z-10">
                <button className="bg-white text-primary px-12 py-5 rounded-2xl font-bold text-xl hover:scale-105 transition-transform shadow-2xl">Start Your Free Trial</button>
              </div>
              {/* Decorative overlay */}
              <div className="absolute top-0 right-0 w-1/2 h-full opacity-10">
                <span className="material-symbols-outlined text-[30rem] rotate-12 select-none">genetics</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-8 py-16 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex flex-col items-center md:items-start gap-4">
            <div className="text-lg font-bold text-slate-900 dark:text-white">DataDNA AI</div>
            <p className="font-['Inter'] text-sm text-slate-500 dark:text-slate-400">© 2024 DataDNA AI. Precision Genomic Fingerprinting.</p>
          </div>
          <div className="flex flex-wrap justify-center gap-8">
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

export default DataDNALanding;
