import React from 'react';

const DataDNATech = () => {
  return (
    <div className="bg-surface text-on-surface selection:bg-primary-fixed selection:text-on-primary-fixed light min-h-screen">
      {/* TopAppBar */}
      <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-xl">
        <div className="flex justify-between items-center max-w-7xl mx-auto px-8 h-20 w-full">
          <div className="text-xl font-bold tracking-tighter text-slate-900">DataDNA AI</div>
          <div className="hidden md:flex items-center gap-8">
            <a className="text-slate-600 hover:text-slate-900 transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Product</a>
            <a className="text-blue-600 font-bold font-['Inter'] tracking-tight" href="#">Technology</a>
            <a className="text-slate-600 hover:text-slate-900 transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Security</a>
            <a className="text-slate-600 hover:text-slate-900 transition-colors font-['Inter'] font-semibold tracking-tight" href="#">Demo</a>
          </div>
          <button className="bg-primary text-on-primary px-6 py-2.5 rounded-xl font-semibold hover:opacity-80 transition-all">
            Get Started
          </button>
        </div>
      </nav>

      <main className="pt-20">
        {/* Hero Section */}
        <section className="py-24 px-8 max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row gap-16 items-center">
            <div className="md:w-1/2">
              <span className="text-primary font-bold tracking-widest text-xs uppercase mb-4 block">The Infrastructure of Trust</span>
              <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter text-on-surface leading-[1.1] mb-8">
                Genomic Precision <br/>AI Watermarking.
              </h1>
              <p className="text-xl text-on-surface-variant max-w-lg mb-10 leading-relaxed">
                DataDNA AI leverages cryptographic hashing and neural fingerprinting to secure every byte of synthetic and proprietary data.
              </p>
              <div className="flex items-center gap-4">
                <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_10px_rgba(0,78,159,0.8)]"></div>
                <span className="text-sm font-medium text-on-surface-variant">Active Processing Node: Global Tier-1</span>
              </div>
            </div>
            <div className="md:w-1/2 w-full aspect-square bg-surface-container-low rounded-[2rem] overflow-hidden relative">
              <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBMwGfR187jO8G2pwVx3WnWs1-9Y9RH16kpVZpY4gjlPLmBHBhv5-ftmD9u6aVcr4xh4UkZKJ36og7ck906yws3sERg9WXjel7J6-aEdcD1blhCSiVt1iXZgq817jwESDFqYCWUt1GhNKDC1XiBqOD0ZE0ukNgsjmXWdVgZlFJjGv0GL1I-Mk7noiU3bjDjgrCrtmzLOQhiCrvoGseMXmvzYf_5XvJm3DpUS1a0T4Uwv6-UE6nWqFZphG2YYXy9wRBDt-zbFDN9PBRc" alt="abstract digital visualization of blue light particles flowing into a crystalline dna structure against a dark background" />
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent"></div>
            </div>
          </div>
        </section>

        {/* Technology Stack Grid */}
        <section className="bg-surface-container-low py-32 px-8">
          <div className="max-w-7xl mx-auto">
            <div className="mb-20">
              <h2 className="text-3xl font-bold tracking-tight mb-4">Core Technology Stack</h2>
              <div className="w-16 h-1 bg-primary"></div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              {/* Tech Card 1 */}
              <div className="group bg-surface-container-lowest p-10 rounded-[2rem] transition-all hover:translate-y-[-4px]">
                <div className="w-14 h-14 bg-surface-container-high rounded-2xl flex items-center justify-center mb-8 text-primary">
                  <span className="material-symbols-outlined text-3xl">bolt</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">FastAPI Core</h3>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  High-performance asynchronous architecture ensuring sub-millisecond response times for massive scale DNA sequencing workloads.
                </p>
                <div className="h-1 w-0 group-hover:w-full bg-primary transition-all duration-500"></div>
              </div>
              
              {/* Tech Card 2 */}
              <div className="group bg-surface-container-lowest p-10 rounded-[2rem] transition-all hover:translate-y-[-4px]">
                <div className="w-14 h-14 bg-surface-container-high rounded-2xl flex items-center justify-center mb-8 text-primary">
                  <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>fingerprint</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">AI Watermarking</h3>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  Invisible metadata embedding directly into neural weights, allowing for identification even after model fine-tuning.
                </p>
                <div className="h-1 w-0 group-hover:w-full bg-primary transition-all duration-500"></div>
              </div>
              
              {/* Tech Card 3 */}
              <div className="group bg-surface-container-lowest p-10 rounded-[2rem] transition-all hover:translate-y-[-4px]">
                <div className="w-14 h-14 bg-surface-container-high rounded-2xl flex items-center justify-center mb-8 text-primary">
                  <span className="material-symbols-outlined text-3xl">token</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Blockchain Ledger</h3>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  Immutable audit trails stored on a private permissioned ledger, providing a tamper-proof history of data provenance.
                </p>
                <div className="h-1 w-0 group-hover:w-full bg-primary transition-all duration-500"></div>
              </div>
            </div>
          </div>
        </section>

        {/* Security Focused Section */}
        <section className="py-32 px-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
            <div className="order-2 lg:order-1">
              <div className="grid grid-cols-2 gap-6">
                <div className="aspect-square rounded-[2rem] overflow-hidden">
                  <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBNC5o6rIWgvzVTQ0FMrdEj7ZUexJNBq6iJzEA_IqxmsVXPgBexRiQ3TOEqHp9VBHvea9B0W4KL2taBvCID0XMXNORISiVNTLTXz_pgFtw9VIzCGbN7ydAhQ5sFncaxt_oGagBgPd7C32eu9twuRBkhHpjdA84zJPqzrDpgSt0IMOORIakr2KMDy_aeGb-cvbGG7pxt3vh503pNx0Lvs8p-4Df9ZamPNCHaFo7ZtswzBFff876wphOhVXbwIsk_MLZ8AQkAK4ZpIkSN" alt="server rack macro shot with blue led status lights reflecting on brushed metal surfaces in a dark data center" />
                </div>
                <div className="aspect-square bg-primary-container rounded-[2rem] flex items-center justify-center p-8">
                  <span className="material-symbols-outlined text-6xl text-on-primary-container" style={{ fontVariationSettings: "'FILL' 1" }}>shield_with_heart</span>
                </div>
                <div className="col-span-2 aspect-[2/1] rounded-[2rem] overflow-hidden">
                  <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBnVoq-MYHtYE82NiD3wtKp-4d2YIIOQvq1RHnFgIc6-o5ix9apah352B9pOKEhqrgZ5z9lTUN9FWYaPPzuhmwasHhSvIDLTx4IBDQn3TAGoPYzIxdKUv-RcdbLREwX0MT0SPZIf1iPGzWIr5wfWg9zkzk8qyNnmELsdyeIj2JMzbt0b9KG1Gqa_2WqB-F1jM0A2BghOm9-p0CexLvDTI8XxfWTFbWv2PC_wHr1Z6ZNRYNjahxCpvL42Ytss12_HHohjZrFYCfaAGFk" alt="dramatic perspective of a modern office ceiling with geometric light patterns creating high contrast shadows" />
                </div>
              </div>
            </div>
            <div className="order-1 lg:order-2">
              <h2 className="text-4xl font-extrabold tracking-tighter mb-12">Fortified Security by Design</h2>
              <div className="space-y-12">
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <span className="material-symbols-outlined text-primary text-3xl">verified_user</span>
                  </div>
                  <div>
                    <h4 className="text-xl font-bold mb-2">Tamper Resistant</h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      Our proprietary 'Drift-Lock' technology detects any modification to watermarked content, automatically invalidating fraudulent credentials in real-time across the network.
                    </p>
                  </div>
                </div>
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <span className="material-symbols-outlined text-primary text-3xl">update</span>
                  </div>
                  <div>
                    <h4 className="text-xl font-bold mb-2">Future-proof AI detection</h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      As Large Language Models evolve, our detection algorithms adapt using adversarial training, ensuring protection against next-generation AI-generated misinformation.
                    </p>
                  </div>
                </div>
                <div className="flex gap-6">
                  <div className="flex-shrink-0">
                    <span className="material-symbols-outlined text-primary text-3xl">lock</span>
                  </div>
                  <div>
                    <h4 className="text-xl font-bold mb-2">Zero-Knowledge Proofs</h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      Verify data authenticity without ever exposing the raw data itself, maintaining the highest standards of enterprise privacy and regulatory compliance.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="mb-32 px-8">
          <div className="max-w-7xl mx-auto bg-slate-900 rounded-[3rem] p-16 md:p-24 text-center overflow-hidden relative">
            <div className="absolute top-0 right-0 w-96 h-96 bg-primary/20 blur-[100px] rounded-full"></div>
            <div className="relative z-10">
              <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-8 tracking-tighter">Ready to secure your data legacy?</h2>
              <p className="text-slate-400 text-lg mb-12 max-w-2xl mx-auto">
                Join the leading AI research labs and financial institutions currently leveraging DataDNA for immutable data fingerprinting.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-primary text-white px-10 py-4 rounded-full font-bold text-lg hover:scale-105 transition-transform">Get a Technical Demo</button>
                <button className="bg-slate-800 text-white px-10 py-4 rounded-full font-bold text-lg hover:bg-slate-700 transition-colors">Read Whitepaper</button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-50 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-8 py-16 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex flex-col items-center md:items-start gap-4">
            <div className="text-lg font-bold text-slate-900">DataDNA AI</div>
            <p className="font-['Inter'] text-sm text-slate-500">© 2024 DataDNA AI. Precision Genomic Fingerprinting.</p>
          </div>
          <div className="flex gap-8">
            <a className="font-['Inter'] text-sm text-slate-500 hover:text-blue-600 transition-colors" href="#">Privacy Policy</a>
            <a className="font-['Inter'] text-sm text-slate-500 hover:text-blue-600 transition-colors" href="#">Terms of Service</a>
            <a className="font-['Inter'] text-sm text-slate-500 hover:text-blue-600 transition-colors" href="#">API Documentation</a>
            <a className="font-['Inter'] text-sm text-slate-500 hover:text-blue-600 transition-colors" href="#">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default DataDNATech;
