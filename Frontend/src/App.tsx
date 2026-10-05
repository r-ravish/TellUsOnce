import { useRef, useState } from 'react';
import {
  ArrowDownRight,
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  Bell,
  BookOpenCheck,
  Check,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  Clock3,
  FileCheck2,
  FileText,
  HeartHandshake,
  Home,
  Paperclip,
  Plus,
  ShieldCheck,
  Sparkles,
  Upload,
} from 'lucide-react';

type Screen = 'overview' | 'requests' | 'documents';

type Service = {
  title: string;
  short: string;
  icon: typeof FileText;
  status: string;
  tone: 'green' | 'coral' | 'yellow' | 'blue';
  office: string;
};

const services: Service[] = [
  { title: 'Attendance condonation', short: 'Attendance', icon: BookOpenCheck, status: 'Needs a document', tone: 'coral', office: 'Academic office' },
  { title: 'Mid-term make-up', short: 'Exam', icon: FileCheck2, status: 'Ready to review', tone: 'yellow', office: 'Examinations' },
  { title: 'Fee deadline extension', short: 'Fees', icon: Clock3, status: 'Being reviewed', tone: 'green', office: 'Student accounts' },
  { title: 'Late hostel return', short: 'Hostel', icon: Home, status: 'Notice prepared', tone: 'blue', office: 'Hostel warden' },
];

const demoStory = 'My father has been seriously ill, so I was away from campus for nine days. I missed a mid-term, my fee deadline is Friday, and I need to let the hostel warden know I will return late.';

const suggestedDocuments = [
  { title: 'Hospital or medical note', detail: 'For your attendance request', state: 'Needed' },
  { title: 'Mid-term details', detail: 'Course name and exam date', state: 'Add details' },
  { title: 'Fee account statement', detail: 'For your extension request', state: 'Optional' },
];

function matchesService(service: Service, story: string) {
  const text = story.toLowerCase();
  switch (service.short) {
    case 'Attendance':
      return /attendance|absence|absent|missed classes|away from campus/.test(text);
    case 'Exam':
      return /exam|mid.?term|test|assessment/.test(text);
    case 'Fees':
      return /fee|tuition|payment|\bpay\b|deadline/.test(text);
    case 'Hostel':
      return /hostel|warden|late return|return late/.test(text);
    default:
      return false;
  }
}

function App() {
  const [screen, setScreen] = useState<Screen>('overview');
  const [story, setStory] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [previewServices, setPreviewServices] = useState<Service[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
  const storyRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const openIntake = () => {
    setScreen('overview');
    setSubmitted(false);
    window.setTimeout(() => storyRef.current?.focus(), 0);
  };

  const submitStory = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (story.trim()) {
      try {
        const response = await fetch("http://localhost:8000/api/intake", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ student_reference: "STUDENT-001", story })
        });
        if (response.ok) {
          const data = await response.json();
          // Map backend response to frontend service format
          const mappedServices = (data.requests || []).map((req: any) => ({
            title: req.request_type.replace(/_/g, " "),
            short: req.request_type,
            icon: FileText,
            status: req.status,
            tone: req.status === "approved" ? "green" : req.status === "escalated" ? "coral" : "blue",
            office: req.department
          }));
          setPreviewServices(mappedServices);
          setSubmitted(true);
        } else {
          console.error("Backend error");
        }
      } catch (err) {
        console.error("Network error: ", err);
      }
    }
  };

  const addFiles = (event: React.ChangeEvent<HTMLInputElement>) => {
    const names = Array.from(event.target.files ?? []).map((file) => file.name);
    setUploadedFiles((current) => [...current, ...names]);
    event.target.value = '';
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#overview" onClick={(event) => { event.preventDefault(); setScreen('overview'); }} aria-label="Tell Us Once home">
          <span className="brand-mark"><span /><span /><span /></span>
          <span className="brand-name">tell us<span>once</span></span>
        </a>
        <div className="campus-label"><span className="campus-dot" /> CAMPUS SERVICES</div>
        <nav className="primary-nav" aria-label="Main navigation">
          <p className="nav-caption">YOUR SPACE</p>
          <button className={`nav-item ${screen === 'overview' ? 'active' : ''}`} onClick={() => setScreen('overview')}>
            <Home size={18} strokeWidth={1.8} /><span>Overview</span>
          </button>
          <button className="nav-item" onClick={openIntake}>
            <Plus size={18} strokeWidth={1.8} /><span>Start a request</span>
          </button>
          <button className={`nav-item ${screen === 'requests' ? 'active' : ''}`} onClick={() => setScreen('requests')}>
            <FileCheck2 size={18} strokeWidth={1.8} /><span>My support plan</span><span className="nav-count">4</span>
          </button>
          <button className={`nav-item ${screen === 'documents' ? 'active' : ''}`} onClick={() => setScreen('documents')}>
            <Paperclip size={18} strokeWidth={1.8} /><span>My documents</span>
          </button>
          <p className="nav-caption nav-caption-spaced">HERE FOR YOU</p>
          <button className="nav-item" onClick={() => document.getElementById('support-note')?.scrollIntoView({ behavior: 'smooth' })}>
            <HeartHandshake size={18} strokeWidth={1.8} /><span>Talk to someone</span>
          </button>
        </nav>
        <div className="sidebar-bottom">
          <div className="support-note" id="support-note">
            <span className="support-icon"><HeartHandshake size={17} /></span>
            <p>Having a difficult day?</p>
            <span>You don't have to figure it out alone.</span>
            <button onClick={() => window.alert('In a live campus portal, this would connect you to the student support team.')}>Find support <ArrowUpRight size={14} /></button>
          </div>
          <button className="profile-row" onClick={() => window.alert('Demo student profile')}>
            <span className="avatar">MR</span>
            <span className="profile-copy"><strong>Maya Rao</strong><small>Student · Year 2</small></span>
            <span className="profile-more">···</span>
          </button>
        </div>
      </aside>

      <div className="main-column">
        <header className="topbar">
          <div className="breadcrumbs"><span>Student services</span><ChevronRight size={15} /><strong>{screen === 'overview' ? 'Overview' : screen === 'requests' ? 'My support plan' : 'My documents'}</strong></div>
          <div className="topbar-actions">
            <span className="term-label"><span className="term-dot" /> Autumn term · 2026</span>
            <button className="icon-button notification-button" aria-label="Notifications" onClick={() => window.alert('You are all caught up.') }><Bell size={18} /><i /></button>
            <span className="topbar-avatar">M</span>
          </div>
        </header>

        <main className="page-content">
          {screen === 'overview' && (
            <>
              <section className="welcome-row">
                <div>
                  <div className="eyebrow"><span className="eyebrow-line" /> A LITTLE LESS TO CARRY</div>
                  <h1>Good morning, Maya<span className="greeting-dot">.</span></h1>
                  <p className="welcome-copy">Whatever's going on, you can start here. We'll help you work out the next step.</p>
                </div>
                <div className="welcome-aside"><span className="sun-mark">✳</span><span>One conversation.<br />A clearer way forward.</span></div>
              </section>

              <section className="intake-layout" aria-labelledby="intake-title">
                <div className="intake-panel">
                  {!submitted ? (
                    <>
                      <div className="panel-heading">
                        <span className="step-number">01</span>
                        <div><p className="section-kicker">START WHERE YOU ARE</p><h2 id="intake-title">Tell us what's going on</h2></div>
                        <span className="private-label"><ShieldCheck size={15} /> Local preview</span>
                      </div>
                      <p className="intake-hint">No forms to figure out. No office names to know. Just say it in your own words.</p>
                      <form onSubmit={submitStory}>
                        <label className="sr-only" htmlFor="story">Describe what's going on</label>
                        <textarea ref={storyRef} id="story" maxLength={1200} value={story} onChange={(event) => setStory(event.target.value)} placeholder="Start anywhere. For example: I've been away caring for a family member and now I'm worried about my exams and fees…" required />
                        <div className="input-foot"><span><ShieldCheck size={14} /> Your story stays in this demo on this device.</span><span>{story.length}/1200</span></div>
                        <div className="form-actions">
                          <button className="button-primary" type="submit" disabled={!story.trim()}>Help me find my next steps <ArrowRight size={16} /></button>
                          <button className="text-button" type="button" onClick={() => setStory(demoStory)}><Sparkles size={15} /> Try an example</button>
                        </div>
                      </form>
                    </>
                  ) : (
                    <div className="review-panel">
                      <div className="panel-heading">
                        <span className="step-number step-complete"><Check size={15} /></span>
                        <div><p className="section-kicker">YOUR STORY, HEARD</p><h2 id="intake-title">{previewServices.length ? 'Here are a few ways we can help' : 'Let’s find the right place to start'}</h2></div>
                      </div>
                      <p className="intake-hint">{previewServices.length ? 'These services may be relevant. Nothing has been sent anywhere; this is a local preview.' : 'This demo could not match your story to a specific office. A person can help you find the right support.'}</p>
                      <div className="review-story"><span className="review-quote">“</span>{story}<button className="edit-story" onClick={() => setSubmitted(false)}>Edit</button></div>
                      <div className="review-results">
                        {previewServices.map((service) => <div className="review-result" key={service.short}><span className={`service-icon ${service.tone}`}><service.icon size={16} /></span><span><strong>{service.title}</strong><small>May involve {service.office}</small></span><CheckCircle2 size={17} className="review-check" /></div>)}
                        {!previewServices.length && <p className="review-empty">You can edit your story to add a few details, or reach out to the student support team.</p>}
                      </div>
                      <div className="review-footer"><span><ShieldCheck size={15} /> Preview only. Nothing has been submitted.</span><button className="button-primary" onClick={() => setScreen('documents')}>See what you'll need <ArrowRight size={16} /></button></div>
                    </div>
                  )}
                </div>
                <aside className="how-panel">
                  <div className="how-top"><span className="how-illustration"><span /><span /><span /></span><span className="how-label">A HUMAN-SIZED PROCESS</span></div>
                  <h2>You only have to<br />tell us <em>once.</em></h2>
                  <p>We'll help connect the dots, so you don't have to explain yourself at every desk.</p>
                  <div className="process-list">
                    <div className="process-item"><span className="process-check"><Check size={12} /></span><span>Your story, in your words</span></div>
                    <div className="process-item"><span className="process-check"><Check size={12} /></span><span>One clear list of next steps</span></div>
                    <div className="process-item"><span className="process-check process-pending"><span /></span><span>The right people, in the loop</span></div>
                  </div>
                  <div className="how-foot"><span className="tiny-shield"><ShieldCheck size={15} /></span><span>People stay part of every important decision.</span></div>
                </aside>
              </section>

              <section className="support-plan-section" id="support-plan" aria-labelledby="plan-title">
                <div className="section-topline"><div><p className="section-kicker">ALL IN ONE PLACE</p><h2 id="plan-title">Your support plan</h2></div><button className="link-button" onClick={() => setScreen('requests')}>View full plan <ArrowRight size={15} /></button></div>
                <article className="case-overview">
                  <div className="case-summary">
                    <div className="case-icon"><HeartHandshake size={19} /></div>
                    <div className="case-title"><span className="case-id">SAMPLE PLAN <span>·</span> TU-2048</span><h3>A few things to sort out</h3><p>Started 2 October · Updated just now</p></div>
                    <span className="case-status"><span /> In progress</span>
                    <button className="case-open" aria-label="Open support plan" onClick={() => setScreen('requests')}><ArrowUpRight size={18} /></button>
                  </div>
                  <div className="case-divider" />
                  <div className="service-grid">
                    {services.map((service) => <div className="service-card" key={service.short}>
                      <span className={`service-icon ${service.tone}`}><service.icon size={17} /></span>
                      <div className="service-copy"><strong>{service.title}</strong><span>{service.office}</span></div>
                      <span className={`service-status ${service.tone}`}><i />{service.status}</span>
                    </div>)}
                  </div>
                  <div className="case-next-step"><span className="next-step-icon"><FileText size={15} /></span><span><strong>Your next step</strong> Add a hospital note to help the academic office review your attendance.</span><button onClick={() => setScreen('documents')}>Add document <ArrowRight size={14} /></button></div>
                </article>
              </section>

              <footer className="page-footer"><span>You're not alone in figuring this out.</span><button onClick={() => document.getElementById('support-note')?.scrollIntoView({ behavior: 'smooth' })}>Reach a real person <ArrowUpRight size={13} /></button><span className="footer-campus">Student services <span>·</span> Here for your next step</span></footer>
            </>
          )}

          {screen === 'requests' && (
            <section className="secondary-page">
              <button className="back-link" onClick={() => setScreen('overview')}><ArrowLeft size={15} /> Overview</button>
              <div className="eyebrow"><span className="eyebrow-line" /> YOUR SUPPORT, TOGETHER</div>
              <h1 className="secondary-title">Your support plan<span className="greeting-dot">.</span></h1>
              <p className="welcome-copy secondary-copy">One situation, a few offices working on it. Here's where things stand.</p>
              <article className="case-overview full-case">
                <div className="case-summary">
                  <div className="case-icon"><HeartHandshake size={19} /></div>
                  <div className="case-title"><span className="case-id">SAMPLE PLAN <span>·</span> TU-2048</span><h3>A few things to sort out</h3><p>Started 2 October · Last updated just now</p></div>
                  <span className="case-status"><span /> In progress</span>
                </div>
                <div className="case-divider" />
                <div className="service-list-full">
                  {services.map((service, index) => <div className="service-row-full" key={service.short}>
                    <span className={`service-icon ${service.tone}`}><service.icon size={18} /></span>
                    <div className="service-copy"><strong>{service.title}</strong><span>{service.office}</span></div>
                    <span className={`service-status ${service.tone}`}><i />{service.status}</span>
                    <button className="row-chevron" aria-label={`View ${service.title}`} onClick={() => setScreen('documents')}><ChevronRight size={17} /></button>
                    {index < services.length - 1 && <span className="row-line" />}
                  </div>)}
                </div>
                <div className="case-next-step"><span className="next-step-icon"><FileText size={15} /></span><span><strong>Next up</strong> Add a hospital note to help the academic office review your attendance.</span><button onClick={() => setScreen('documents')}>Add document <ArrowRight size={14} /></button></div>
              </article>
              <section className="timeline-section"><div className="section-topline"><div><p className="section-kicker">WHAT'S HAPPENED</p><h2>A little progress, step by step</h2></div></div>
                <div className="timeline"><div className="timeline-entry"><span className="timeline-mark done"><Check size={12} /></span><div><strong>Your support plan was created</strong><p>All four requests are together in one place.</p></div><time>2 Oct</time></div><div className="timeline-entry"><span className="timeline-mark active"><span /></span><div><strong>Fee extension sent for review</strong><p>Student accounts will follow up on your request.</p></div><time>Today</time></div><div className="timeline-entry"><span className="timeline-mark waiting"><Clock3 size={13} /></span><div><strong>Attendance request needs a document</strong><p>Add a hospital note when you're ready.</p></div><time>Waiting on you</time></div></div>
              </section>
              <footer className="page-footer"><span>Need a hand with any of this?</span><button onClick={() => window.alert('In a live campus portal, this would connect you to the student support team.')}>Talk to someone <ArrowUpRight size={13} /></button></footer>
            </section>
          )}

          {screen === 'documents' && (
            <section className="secondary-page">
              <button className="back-link" onClick={() => setScreen('overview')}><ArrowLeft size={15} /> Overview</button>
              <div className="eyebrow"><span className="eyebrow-line" /> YOUR DOCUMENTS</div>
              <h1 className="secondary-title">One place for the paperwork<span className="greeting-dot">.</span></h1>
              <p className="welcome-copy secondary-copy">See what's needed, what's optional, and what you can add when you're ready.</p>
              <div className="document-layout">
                <section className="document-panel">
                  <div className="section-topline"><div><p className="section-kicker">SUPPORT PLAN · TU-2048</p><h2>What would help</h2></div><span className="doc-count">1 of 3 ready</span></div>
                  <div className="document-checklist">
                    {suggestedDocuments.map((document) => {
                      const isUploaded = uploadedFiles.length > 0 && document.title === 'Hospital or medical note';
                      return <div className="document-row" key={document.title}><span className={`doc-status-icon ${isUploaded ? 'uploaded' : ''}`}>{isUploaded ? <Check size={15} /> : <FileText size={17} />}</span><div className="doc-copy"><strong>{document.title}</strong><span>{document.detail}</span></div><span className={`doc-badge ${isUploaded ? 'complete' : document.state === 'Needed' ? 'needed' : 'optional'}`}>{isUploaded ? 'Added' : document.state}</span></div>;
                    })}
                  </div>
                  {uploadedFiles.length > 0 && <div className="uploaded-files">{uploadedFiles.map((file, index) => <span className="uploaded-file" key={`${file}-${index}`}><Paperclip size={13} />{file}</span>)}</div>}
                  <input ref={fileInputRef} className="sr-only" type="file" multiple onChange={addFiles} aria-label="Choose documents to upload" />
                  <button className="upload-button" onClick={() => fileInputRef.current?.click()}><Upload size={16} /> Add a document <Plus size={15} /></button>
                  <p className="document-privacy"><ShieldCheck size={15} /> This is a demo. Files you choose are not uploaded or saved.</p>
                </section>
                <aside className="document-side-note"><span className="note-art"><FileCheck2 size={22} /></span><p className="section-kicker">A SMALL REMINDER</p><h2>You can add things later.</h2><p>You don't need every document to get started. Share what you have, and we'll help you figure out the rest.</p><button onClick={() => setScreen('requests')}>Back to my support plan <ArrowRight size={15} /></button></aside>
              </div>
              <footer className="page-footer"><span>Not sure what a document means?</span><button onClick={() => window.alert('In a live campus portal, this would connect you to the student support team.')}>Ask for help <ArrowUpRight size={13} /></button></footer>
            </section>
          )}
        </main>
      </div>
      <button className="help-fab" aria-label="Get help" onClick={() => window.alert('In a live campus portal, this would connect you to the student support team.')}><CircleHelp size={19} /><span>Need help?</span><ArrowDownRight size={14} /></button>
    </div>
  );
}

export default App;

