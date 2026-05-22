import os
import subprocess
import sys

def install_reportlab():
    print("[Setup] Checking reportlab installation...")
    try:
        import reportlab
        print("[Setup] reportlab is already installed.")
    except ImportError:
        print("[Setup] reportlab not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        print("[Setup] reportlab installed successfully.")

def delete_old_papers(data_dir="data"):
    print("[Cleanup] Cleaning up old documents...")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"[Cleanup] Created data directory at {data_dir}")
        return

    # Delete all PDF files to ensure clean regeneration of all 20 papers
    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(data_dir, file)
            try:
                os.remove(file_path)
                print(f"[Cleanup] Removed: {file}")
            except Exception as e:
                print(f"[Cleanup] Error removing {file}: {e}")

def create_pdfs(data_dir="data"):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    
    print("[Generation] Generating 20 legal, tax, and compliance PDFs...")
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=15,
        textColor="#1E3A8A"
    )
    
    heading_style = ParagraphStyle(
        'DocHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        spaceBefore=12,
        spaceAfter=6,
        textColor="#0F172A",
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        textColor="#334155"
    )

    documents = [
        {
            "filename": "Delaware_LLC_Agreement_Sample.pdf",
            "title": "LIMITED LIABILITY COMPANY AGREEMENT",
            "subtitle": "OF NEXUS VENTURES LLC (A DELAWARE LLC)",
            "sections": [
                ("Section 3: CAPITAL CONTRIBUTIONS", "3.1 Capital Accounts. A separate capital account shall be maintained for each Member. Capital contributions shall be made in cash or other tangible property as agreed by a majority of Members. No member shall be required to make any additional capital contributions unless unanimously approved."),
                ("Section 4: MANAGEMENT AND VOTING", "4.1 Manager-Managed Structure. The business and affairs of the Company shall be managed exclusively by a designated Manager. John Doe is hereby designated as the initial Manager. The Manager shall hold office until a successor is elected by a Majority Vote of the Members. 4.2 Authority of Manager. The Manager has the authority to bind the Company in the ordinary course of business. Any transaction exceeding fifty thousand dollars ($50,000) requires the prior written approval of Members holding at least 75% of the voting interests."),
                ("Section 8: INDEMNIFICATION AND LIABILITY LIMITATION", "8.1 Limitation of Liability. To the fullest extent permitted by the Delaware General Corporation Law and the Delaware Limited Liability Company Act, no Manager or Officer of the Company shall be personally liable to the Company or its Members for monetary damages for breach of fiduciary duty. 8.2 Indemnification. The Company shall indemnify, defend, and hold harmless the Manager and Members from and against any and all claims, demands, liabilities, losses, damages, and expenses (including reasonable attorneys' fees) arising out of or in connection with the operations of the Company, provided that the indemnified person acted in good faith and without gross negligence or willful misconduct."),
                ("Section 11: GOVERNING LAW AND RESOLUTION", "11.1 Delaware Law. This Agreement, and all claims or causes of action arising hereunder, shall be governed by, and construed in accordance with, the laws of the State of Delaware, without giving effect to conflict of laws principles. All legal actions shall be brought in the Court of Chancery of the State of Delaware.")
            ]
        },
        {
            "filename": "Corporate_Code_of_Conduct_Policy.pdf",
            "title": "GLOBAL CODE OF CONDUCT & ETHICS POLICY",
            "subtitle": "VERTEX CORP & CONTROLLED SUBSIDIARIES",
            "sections": [
                ("Section 1: SCOPE AND GENERAL OBLIGATIONS", "1.1 Applicability. This Policy applies to all full-time employees, part-time employees, officers, directors, and independent contractors of Vertex Corp worldwide. Every representative must review and sign this policy annually."),
                ("Section 2: ANTI-BRIBERY AND FCPA COMPLIANCE", "2.1 Prohibited Payments. Vertex Corp has zero tolerance for bribery and corruption. In accordance with the U.S. Foreign Corrupt Practices Act (FCPA) and local laws, representatives are strictly prohibited from offering, paying, promising, or authorizing the payment of any money, gift, travel expense, or thing of value to any foreign official, political candidate, or government employee to influence an official act or secure an improper business advantage. 2.2 Accounting Standards. All transactions must be accurately recorded in the corporate books. Slush funds or off-book transactions are strictly illegal. Violation of anti-bribery policies will result in immediate termination and referral to law enforcement agencies."),
                ("Section 3: CONFLICTS OF INTEREST", "3.1 Mandatory Disclosure. Employees must avoid situations where their personal interests conflict with Vertex Corp. Conflict situations include holding a financial stake in a vendor or competitor, or undertaking external employment. All potential conflicts must be disclosed in writing to the Compliance Officer (compliance@vertexcorp.com) for review and resolution."),
                ("Section 4: WHISTLEBLOWER PROTECTION AND NON-RETALIATION", "4.1 Reporting Violations. Employees are encouraged to report any suspected compliance violations, financial fraud, or unethical behavior. Reports can be made anonymously through the secure compliance hotline (1-800-555-ETHX). 4.2 Non-Retaliation Policy. Vertex Corp maintains a strict non-retaliation policy. No employee shall be demoted, harassed, threatened, or penalized for making a report in good faith. Any retaliatory actions will face severe disciplinary consequences.")
            ]
        },
        {
            "filename": "IRS_Tax_Instructions_Excerpt.pdf",
            "title": "FEDERAL TAX COMPLIANCE AND AUDIT INSTRUCTIONS",
            "subtitle": "EXCERPT FOR CORPORATE AUDITORS",
            "sections": [
                ("Section A: ORDINARY AND NECESSARY BUSINESS EXPENSES", "Under Internal Revenue Code (IRC) Section 162, corporate entities may deduct ordinary and necessary expenses paid or incurred during the taxable year in carrying on any trade or business. Ordinary expenses are defined as those that are common and accepted in the taxpayer's business community. Necessary expenses are defined as those that are helpful and appropriate for the business."),
                ("Section B: BUSINESS MEALS AND ENTERTAINMENT RESTRICTIONS", "B.1 Entertainment Deductions. In accordance with current tax guidelines, corporate deductions for entertainment, amusement, or recreation expenses are generally 100% disallowed. B.2 Business Meal Deductions. Deductions for business meals are limited to a 50% deduction rate. To qualify, the meal must not be lavish or extravagant under the circumstances, and the taxpayer (or an employee) must be present at the time the food or beverages are provided. Documentation must verify the business purpose and attendees."),
                ("Section C: SECTION 179 EXPENSING LIMITS AND PROPERTY RULES", "C.1 Expense Limits. The maximum amount a taxpayer may elect to expense under Section 179 for the taxable year is $1,160,000. This threshold is reduced dollar-for-dollar by the amount by which the total cost of Section 179 property placed in service exceeds $2,890,000."),
                ("Section D: AUDIT DOCUMENTATION AND RETENTION PROTOCOL", "D.1 Record Retention Period. To ensure compliance with IRS audit protocols, all corporate taxpayers are mandated to retain tax returns, invoices, sales receipts, bank statements, ledger books, and payroll records for a minimum period of seven (7) years from the date of filing. Failure to provide documentation during an audit will result in disallowance of deductions, tax reassessments, and accuracy-related penalties.")
            ]
        },
        {
            "filename": "Non_Disclosure_Agreement_Sample.pdf",
            "title": "MUTUAL NON-DISCLOSURE AND CONFIDENTIALITY AGREEMENT",
            "subtitle": "STANDARD BILATERAL BUSINESS EXCHANGE NDA",
            "sections": [
                ("Section 1: DEFINITION OF CONFIDENTIAL INFORMATION", "1.1 Scope. Confidential Information refers to any proprietary data, trade secrets, software, designs, or financial information disclosed by one Party to the other. To be protected, it must be marked as confidential or disclosed under circumstances where a reasonable person would understand its confidential nature."),
                ("Section 2: TERM AND NON-USE OBLIGATIONS", "2.1 Confidentiality Period. The receiving Party agrees to hold and maintain Confidential Information in strict trust for a period of three (3) years from the date of disclosure. During this term, the receiving Party shall not use the information for any purpose other than evaluating a potential business relationship."),
                ("Section 4: EQUITABLE RELIEF AND REMEDIES", "4.1 Injunctive Relief. In the event of a breach or threatened breach of this Agreement, the disclosing Party shall be entitled to seek injunctive relief, specific performance, or other equitable remedies without the necessity of posting a bond, in addition to any monetary damages.")
            ]
        },
        {
            "filename": "GDPR_Privacy_Compliance_Policy.pdf",
            "title": "GENERAL DATA PROTECTION REGULATION (GDPR) POLICY",
            "subtitle": "EU RESIDENT DATA PROTECTION AND PRIVACY STANDARD",
            "sections": [
                ("Article 4: SCOPE OF DATA PROCESSING", "This policy outlines data processing standards for personal data belonging to EU data subjects. Vertex Corp acts as a Data Controller. Processing is restricted to lawful bases under GDPR Article 6, including consent, contractual necessity, or legitimate interest."),
                ("Article 15-21: DATA SUBJECT RIGHTS", "EU residents have the right to request access to, rectification of, or erasure of their personal data (Right to be Forgotten). Vertex Corp must respond to all verified requests within thirty (30) calendar days without charge."),
                ("Article 33: MANDATORY 72-HOUR BREACH NOTIFICATION", "In the event of a personal data breach that risks the rights and freedoms of individuals, the Compliance Officer must notify the relevant Supervisory Authority within seventy-two (72) hours of becoming aware of the breach.")
            ]
        },
        {
            "filename": "CCPA_Consumer_Privacy_Guidelines.pdf",
            "title": "CALIFORNIA CONSUMER PRIVACY ACT (CCPA) COMPLIANCE",
            "subtitle": "STATUTORY DISCLOSURE & DATA PRIVACY INSTRUCTIONS",
            "sections": [
                ("Section 1: NOTICE AT COLLECTION AND RIGHT TO OPT-OUT", "Vertex Corp must notify California residents at or before the point of data collection regarding the categories of personal information collected. Consumers have the absolute right to opt-out of the sale or sharing of their personal information via a prominent link labeled 'Do Not Sell My Personal Information' on the homepage."),
                ("Section 2: RIGHT TO DELETE AND ACCESS", "Consumers have the right to request deletion of personal information collected from them. Vertex Corp must verify the consumer's identity and fulfill requests within forty-five (45) days of receipt, with a one-time extension of an additional 45 days if reasonably necessary."),
                ("Section 4: CIVIL PENALTIES FOR VIOLATIONS", "The California Attorney General or the California Privacy Protection Agency (CPPA) may seek civil penalties of up to $2,500 for each non-intentional violation and up to $7,500 for each intentional violation of CCPA rules.")
            ]
        },
        {
            "filename": "HIPAA_Security_Rule_Standard.pdf",
            "title": "HIPAA SECURITY AND BREACH NOTIFICATION STANDARDS",
            "subtitle": "PROTECTED HEALTH INFORMATION (PHI) SECURITY RULES",
            "sections": [
                ("Section 1: ADMINISTRATIVE SAFEGUARDS", "All business associates and covered entities must perform a formal, documented security risk analysis annually. Mandatory training programs must be conducted for all staff handling Protected Health Information (PHI)."),
                ("Section 2: TECHNICAL SAFEGUARDS & ACCESS CONTROLS", "Access to electronic PHI (ePHI) must be limited to authorized personnel with unique user logins. Encryption must be implemented for ePHI both in transit (e.g., SSL/TLS) and at rest (e.g., AES-256) unless a documented alternative is implemented."),
                ("Section 3: BREACH NOTIFICATION RULE", "Breaches of unsecured PHI affecting five hundred (500) or more individuals require immediate notification to the Department of Health and Human Services (HHS) and local media outlets within sixty (60) days of discovery. Smaller breaches must be logged and reported annually.")
            ]
        },
        {
            "filename": "Anti_Money_Laundering_AML_Policy.pdf",
            "title": "ANTI-MONEY LAUNDERING AND KYC COMPLIANCE POLICY",
            "subtitle": "FINANCIAL SERVICES COMPLIANCE AND AUDIT STANDARDS",
            "sections": [
                ("Section 1: CUSTOMER IDENTIFICATION PROGRAM (CIP)", "To prevent money laundering, Vertex Financials must verify the identity of every customer opening an account. CIP requires verifying the customer's full legal name, date of birth, physical address, and government-issued ID number before conducting transactions."),
                ("Section 2: SUSPICIOUS ACTIVITY REPORTING (SAR)", "Employees must report any transaction or series of transactions exceeding ten thousand dollars ($10,000) that seems suspicious. A Suspicious Activity Report (SAR) must be filed with FinCEN within thirty (30) calendar days of detecting the suspicious behavior."),
                ("Section 3: RECORD KEEPING AND AUDIT", "All AML and CIP records, including customer identification records and filed SARs, must be retained for a minimum of five (5) years after the account is closed. Independent audits of the AML program must be conducted annually.")
            ]
        },
        {
            "filename": "FCPA_Anti_Corruption_Guidelines.pdf",
            "title": "FOREIGN CORRUPT PRACTICES ACT (FCPA) COMPLIANCE POLICY",
            "subtitle": "ANTI-CORRUPTION & GIFTS STANDARDS FOR MULTINATIONAL OPERATIONS",
            "sections": [
                ("Section 1: PROHIBITION OF IMPROPER PAYMENTS", "No representative of Vertex Corp may pay, offer, or promise anything of value to a foreign government official to obtain or retain business. This prohibition covers cash, gifts, entertainment, and charitable donations made on behalf of an official."),
                ("Section 2: BOOKS AND RECORDS ACCOUNTING MANDATE", "Vertex Corp must maintain books, records, and accounts that accurately and fairly reflect all transactions and dispositions of corporate assets. Internal accounting controls must be designed to prevent off-book transactions and unauthorized asset transfers."),
                ("Section 3: DUE DILIGENCE ON THIRD PARTIES", "Before engaging joint ventures, agents, or consultants in foreign markets, comprehensive due diligence must be conducted to verify their reputation and confirm they have no history of corrupt practices. Standard FCPA compliance clauses must be included in all contracts.")
            ]
        },
        {
            "filename": "ERISA_Retirement_Plan_Summary.pdf",
            "title": "EMPLOYEE RETIREMENT INCOME SECURITY ACT (ERISA) COMPLIANCE",
            "subtitle": "SUMMARY OF FIDUCIARY DUTIES AND PLAN REPORTING",
            "sections": [
                ("Section 1: FIDUCIARY DUTIES & STANDARDS OF CONDUCT", "Fiduciaries of ERISA-regulated retirement plans must act solely in the interest of plan participants and beneficiaries. They must exercise the care, skill, prudence, and diligence of a prudent person acting in a like capacity, and diversify plan investments to minimize risk."),
                ("Section 2: ANNUAL REPORTING & FORM 5500", "Plan administrators must file Form 5500 annually with the Department of Labor (DOL) by the last day of the seventh month after the plan year ends. Late filings or failure to file can result in steep civil penalties and audit triggers."),
                ("Section 3: PARTICIPANT DISCLOSURES", "Fiduciaries are required to provide plan participants with a Summary Plan Description (SPD) explaining plan rules, benefits, and rights within ninety (90) days of becoming a participant, and an updated SPD every five (5) years.")
            ]
        },
        {
            "filename": "OSHA_Workplace_Safety_Rules.pdf",
            "title": "OCCUPATIONAL SAFETY AND HEALTH ACT (OSHA) RULES",
            "subtitle": "GENERAL SAFETY COMPLIANCE & INCIDENT REPORTING",
            "sections": [
                ("Section 1: GENERAL DUTY CLAUSE", "Under Section 5(a)(1) of the Occupational Safety and Health Act, every employer must furnish to each employee a place of employment free from recognized hazards that cause or are likely to cause death or serious physical harm."),
                ("Section 2: INCIDENT REPORTING TIMELINES", "Employers must report any work-related fatality to OSHA within eight (8) hours. Any work-related inpatient hospitalization, amputation, or loss of an eye must be reported to OSHA within twenty-four (24) hours of the incident."),
                ("Section 3: SAFETY LOGKEEPING (FORM 300)", "Employers with more than ten (10) employees must maintain OSHA Form 300 logs to record all recordable work-related injuries and illnesses. These logs must be kept on-site for five (5) years and posted annually from February 1 to April 30.")
            ]
        },
        {
            "filename": "IP_Assignment_and_Invention_Agreement.pdf",
            "title": "PROPRIETARY INFORMATION AND INVENTIONS AGREEMENT",
            "subtitle": "INTELLECTUAL PROPERTY ASSIGNMENT CONTRACT FOR EMPLOYEES",
            "sections": [
                ("Section 1: PROPRIETARY INFORMATION AND CONFIDENTIALITY", "The Employee agrees to keep all non-public, proprietary technical and business information of Vertex Corp strictly confidential during and after employment, using it only for the benefit of the Company."),
                ("Section 2: ASSIGNMENT OF INVENTIONS", "The Employee hereby assigns to the Company all rights, titles, and interests in any inventions, designs, software, or improvements developed during employment. This assignment applies to work created on company time, using company resources, or relating to the company's business."),
                ("Section 3: WORK MADE FOR HIRE", "Any original works of authorship created by the Employee within the scope of employment are deemed 'works made for hire' under the U.S. Copyright Act. Ownership of copyrights in such works belongs automatically and exclusively to the Company.")
            ]
        },
        {
            "filename": "Joint_Venture_Agreement_Draft.pdf",
            "title": "JOINT VENTURE PARTNERSHIP AGREEMENT",
            "subtitle": "STRATEGIC VENTURE FORMATION PROTOCOL",
            "sections": [
                ("Section 2: CAPITAL CONTRIBUTION AND RATIOS", "Partner A and Partner B shall contribute capital in a 60/40 ratio. Total initial capital is set at five million dollars ($5,000,000). Profits, losses, and voting rights shall be divided in proportion to each partner's capital share."),
                ("Section 5: MANAGEMENT AND DEADLOCK RESOLUTION", "A Management Board consisting of five members (three appointed by Partner A, two by Partner B) shall oversee the Joint Venture. In the event of a board deadlock, the matter shall be referred to the chief executive officers of both partners for mediation."),
                ("Section 9: TRANSFER RESTRICTIONS & EXIT", "Neither Partner may sell, transfer, or pledge its interest in the Joint Venture without the prior written consent of the other Partner. A Right of First Refusal applies if a Partner receives a bona fide purchase offer from a third party.")
            ]
        },
        {
            "filename": "IRS_W9_Instructional_Guide.pdf",
            "title": "TAXPAYER IDENTIFICATION NUMBER & CERTIFICATION GUIDE",
            "subtitle": "FORM W-9 INSTRUCTIONS AND COMPLIANCE RULES",
            "sections": [
                ("Section 1: PURPOSE OF FORM W-9", "Form W-9 is used by individuals and entities to certify their correct Taxpayer Identification Number (TIN) or Social Security Number (SSN) to requesting parties who must file information returns with the IRS."),
                ("Section 2: BACKUP WITHHOLDING MANDATE", "A payee who fails to provide a correct TIN or fails to certify their exemption may be subject to backup withholding at a flat rate of twenty-four percent (24%) on certain payments. Payees must certify under penalties of perjury that they are not subject to backup withholding."),
                ("Section 3: PENALTIES FOR MISREPRESENTATION", "A payee who makes a false statement on a Form W-9 with no reasonable basis that results in no backup withholding is subject to a five hundred dollar ($500) civil penalty, and intentional fraud may result in criminal prosecution.")
            ]
        },
        {
            "filename": "Form_1099_NEC_Filing_Instructions.pdf",
            "title": "NONEMPLOYEE COMPENSATION REPORTING COMPLIANCE",
            "subtitle": "FORM 1099-NEC FILING AND PENALTY SYSTEM",
            "sections": [
                ("Section A: REPORTING THRESHOLD AND RECIPIENTS", "Payers must file Form 1099-NEC for each person in the course of business to whom they paid at least six hundred dollars ($600) for services performed by a nonemployee (independent contractor) during the calendar year."),
                ("Section B: FILING DEADLINES", "The statutory deadline for filing Form 1099-NEC with the IRS and providing a copy to the recipient is January 31 of the year following the payment. This deadline applies to both paper and electronic filings, with no automatic extensions allowed."),
                ("Section C: LATE FILING PENALTIES", "Failure to file correct information returns on time results in tiered penalties: fifty dollars ($50) per return filed within 30 days late, one hundred ten dollars ($110) per return filed more than 30 days late but by August 1, and two hundred ninety dollars ($290) after August 1.")
            ]
        },
        {
            "filename": "IRS_Audit_Survival_Best_Practices.pdf",
            "title": "TAXPAYER AUDIT SURVIVAL AND APPEALS GUIDE",
            "subtitle": "STRATEGY FOR CORRESPONDENCE AND FIELD AUDITS",
            "sections": [
                ("Section 1: TYPES OF AUDITS AND EXPECTATIONS", "IRS audits are conducted in three ways: Correspondence audits (by mail), Office audits (at an IRS office), and Field audits (at the taxpayer's home or office). Field audits represent the highest level of scrutiny and require careful prep."),
                ("Section 2: BURDEN OF PROOF AND DOCUMENTATION", "The burden of proof during an audit rests entirely on the taxpayer. Taxpayers must produce invoices, bank statements, receipts, and mileage logs to substantiate all claimed business deductions. Receipts are mandatory for all deductions over seventy-five dollars ($75)."),
                ("Section 3: APPEALING IRS AUDIT FINDINGS", "If a taxpayer disagrees with the auditor's findings, they have thirty (30) days from receiving the IRS examination report to file an appeal with the IRS Office of Appeals. A formal written protest must state the tax years and specific issues disputed.")
            ]
        },
        {
            "filename": "SOC_2_Type_II_Security_Standard.pdf",
            "title": "SYSTEM AND ORGANIZATION CONTROLS (SOC) 2 COMPLIANCE",
            "subtitle": "TRUST SERVICES CRITERIA AUDIT PROTOCOL",
            "sections": [
                ("Section A: TRUST SERVICES CRITERIA SCOPE", "SOC 2 reports evaluate controls relevant to Security, Availability, Processing Integrity, Confidentiality, and Privacy. Security (Common Criteria) is the only mandatory criterion and focuses on protection against unauthorized access."),
                ("Section B: TYPE I VS TYPE II AUDITS", "A SOC 2 Type I report evaluates the suitability of control design at a single point in time. A SOC 2 Type II report evaluates the operating effectiveness of controls over a minimum testing period of six (6) to twelve (12) consecutive months."),
                ("Section C: AUDIT PREPARATION AND MONITORING", "Organizations undergoing a Type II audit must provide continuous evidence of control execution, including system logs, change management records, and employee training compliance. Gaps in logs will result in qualified opinions.")
            ]
        },
        {
            "filename": "Section_409A_Valuation_Guidelines.pdf",
            "title": "IRC SECTION 409A DEFERRED COMPENSATION RULES",
            "subtitle": "SAFE HARBOR VALUATION PROTOCOL FOR STARTUPS",
            "sections": [
                ("Section A: SCOPE AND DEFINITION OF 409A", "Internal Revenue Code Section 409A governs non-qualified deferred compensation. It mandates that stock options granted to employees must have an exercise price equal to or greater than the fair market value of the underlying common stock on the grant date."),
                ("Section B: SAFE HARBOR VALUATION METHOD", "To establish fair market value, companies can use a 'Safe Harbor' valuation method, most commonly an independent appraisal by a qualified valuation firm. A Safe Harbor valuation remains valid for a maximum of twelve (12) months or until a material event occurs."),
                ("Section C: PENALTIES FOR NON-COMPLIANCE", "If stock options are issued with an exercise price below fair market value, the options fail to comply with Section 409A. The recipient faces immediate income taxation, a twenty percent (20%) federal excise tax, interest penalties, and state-level penalties.")
            ]
        },
        {
            "filename": "Delaware_Corporate_Bylaws_Template.pdf",
            "title": "CORPORATE BYLAWS OF VERTEX INDUSTRIES INC",
            "subtitle": "DELAWARE CORPORATION GOVERNING CHARTER",
            "sections": [
                ("Article II: STOCKHOLDERS MEETINGS", "The annual meeting of stockholders for the election of directors shall be held on the first Tuesday of May. Special meetings of stockholders may be called at any time by the Board of Directors or by stockholders holding at least ten percent (10%) of outstanding shares."),
                ("Article III: BOARD OF DIRECTORS AND QUORUM", "The business of the Corporation shall be managed by a Board of Directors. A majority of the total number of directors shall constitute a quorum for the transaction of business. Directors may participate in board meetings via teleconference."),
                ("Article VI: SHARE CERTIFICATES & RESTRICTIONS", "Shares of stock may be represented by certificates or be uncertificated. The transfer of stock is subject to any restrictions contained in stockholder agreements or bylaws. Shareholders must notify the secretary before transferring shares to external parties.")
            ]
        },
        {
            "filename": "Employee_Handbook_Compliance_Summary.pdf",
            "title": "EMPLOYEE HANDBOOK COMPLIANCE FRAMEWORK",
            "subtitle": "STATUTORY EMPLOYMENT POLICIES AND DISCLOSURES",
            "sections": [
                ("Section 1: AT-WILL EMPLOYMENT RELATIONSHIP", "Employment with Vertex Corp is at-will, meaning either the employee or the company may terminate the employment relationship at any time, with or without cause or prior notice. No manager has the authority to make any agreement to the contrary."),
                ("Section 2: ANTI-HARASSMENT AND EEO POLICY", "Vertex Corp is an Equal Opportunity Employer. Harassment, discrimination, or retaliation based on race, color, religion, sex, age, national origin, or disability is strictly prohibited. Violations must be reported to HR immediately for investigation."),
                ("Section 3: FAMILY AND MEDICAL LEAVE ACT (FMLA)", "Under the federal FMLA, employees who have completed twelve (12) months of service and worked at least 1,250 hours are eligible for up to twelve (12) weeks of unpaid, job-protected leave per year for specified family and medical reasons.")
            ]
        }
    ]

    for doc_info in documents:
        path = os.path.join(data_dir, doc_info["filename"])
        doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
        story = []
        
        # Build document contents
        story.append(Paragraph(doc_info["title"], title_style))
        story.append(Paragraph(doc_info["subtitle"], ParagraphStyle('Subtitle', parent=title_style, fontSize=11, spaceAfter=20)))
        story.append(Spacer(1, 10))
        
        for heading, body in doc_info["sections"]:
            story.append(Paragraph(heading, heading_style))
            story.append(Paragraph(body, body_style))
            
        doc.build(story)
        print(f"[Success] Generated: {path}")

if __name__ == "__main__":
    install_reportlab()
    delete_old_papers()
    create_pdfs()
    print("[Success] All 20 legal/compliance papers generated successfully.")
