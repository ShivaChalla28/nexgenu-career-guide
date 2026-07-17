import os
import json
from database import SessionLocal, engine, Base
from models import Career, Roadmap, Branch, BranchCareerMap

def seed():
    # Attempt to create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if branch exists or create it
        branches = [
            "Computer Science Engineering (CSE)",
            "Information Technology (IT)",
            "Artificial Intelligence & Data Science",
            "Electronics & Communication Engineering (ECE)",
            "Electrical & Electronics Engineering (EEE)",
            "Mechanical Engineering (Career Transition)",
            "Civil Engineering (Career Transition)",
            "Any Engineering Graduate with Programming Skills"
        ]
        
        db_branches = []
        for b_name in branches:
            b = db.query(Branch).filter(Branch.name == b_name).first()
            if not b:
                b = Branch(name=b_name, slug=b_name.lower().replace(" ", "-").replace("&", "and").replace("(", "").replace(")", ""))
                db.add(b)
                db.commit()
                db.refresh(b)
            db_branches.append(b)

        # ----------------------------------------------------------------
        # Helper Function to Seed Careers
        # ----------------------------------------------------------------
        def seed_career(career_data, roadmap_data):
            career = db.query(Career).filter(Career.name == career_data["name"]).first()
            if not career:
                career = Career(**career_data)
                db.add(career)
                db.commit()
                db.refresh(career)

                for b in db_branches:
                    # Some careers might only apply to specific branches, but for now we apply to all listed
                    bcm = db.query(BranchCareerMap).filter(BranchCareerMap.branch_id == b.id, BranchCareerMap.career_id == career.id).first()
                    if not bcm:
                        bcm = BranchCareerMap(branch_id=b.id, career_id=career.id)
                        db.add(bcm)
                db.commit()

            roadmap = db.query(Roadmap).filter(Roadmap.career_id == career.id).first()
            if not roadmap:
                roadmap_data["career_id"] = career.id
                roadmap = Roadmap(**roadmap_data)
                db.add(roadmap)
                db.commit()
                print(f"Successfully inserted {career_data['name']} role and roadmap.")
            else:
                print(f"{career_data['name']} already exists.")

        # ----------------------------------------------------------------
        # 1. Software Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Software Engineer",
                "slug": "software-engineer",
                "overview": "Career Category: Software Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–8 LPA, Mid-Level: ₹8–18 LPA, Senior: ₹20–50+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Apple, Adobe, Oracle, IBM, Infosys, TCS, Accenture, Capgemini, Cognizant",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Software Engineer Complete Roadmap",
                "description": "Stop guessing your future. NexGenU Career Vision Roadmaps guides engineering students step-by-step from beginner to industry-ready professional.",
                "skills_matrix": {
                    "Programming Languages": ["Java (Recommended)", "Python (Alternative)", "C Programming", "JavaScript (Basics)"],
                    "Computer Science Fundamentals": ["Data Structures", "Algorithms", "OOP", "OS", "DBMS", "Computer Networks", "Software Engineering Concepts"],
                    "Database": ["SQL", "MySQL / PostgreSQL"],
                    "Version Control": ["Git", "GitHub"],
                    "Development Tools": ["Visual Studio Code", "IntelliJ IDEA", "PyCharm"],
                    "Web Basics": ["HTML5", "CSS3", "REST APIs"],
                    "Software Development": ["Debugging", "Unit Testing", "Agile Methodology", "SDLC", "Code Review"],
                    "Soft Skills": ["Communication", "Problem Solving", "Analytical Thinking", "Teamwork", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Operating Systems", "Internet Basics", "File Management", "SDLC Introduction"]},
                    {"phase": 2, "title": "Programming Fundamentals", "duration": "4 Weeks", "learn": ["Variables", "Data Types", "Operators", "Conditional Statements", "Loops", "Functions", "Arrays", "Strings", "File Handling", "Exception Handling"]},
                    {"phase": 3, "title": "Object-Oriented Programming", "duration": "2 Weeks", "learn": ["Classes", "Objects", "Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "Interfaces"]},
                    {"phase": 4, "title": "Data Structures & Algorithms", "duration": "8 Weeks", "learn": ["Arrays", "Strings", "Linked Lists", "Trees", "Graphs", "Sorting", "Searching", "Dynamic Programming", "Greedy"]},
                    {"phase": 5, "title": "Database (SQL)", "duration": "3 Weeks", "learn": ["SQL Basics", "CRUD Operations", "Joins", "Aggregate Functions", "Views", "Indexes", "Normalization"]},
                    {"phase": 6, "title": "Operating Systems", "duration": "2 Weeks", "learn": ["Process", "Thread", "Scheduling", "Memory Management", "Deadlocks", "Virtual Memory", "File System"]},
                    {"phase": 7, "title": "Computer Networks", "duration": "2 Weeks", "learn": ["TCP/IP", "HTTP", "HTTPS", "DNS", "Routing", "REST APIs"]},
                    {"phase": 8, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request", "Collaboration"]},
                    {"phase": 9, "title": "Software Engineering", "duration": "2 Weeks", "learn": ["SDLC", "Agile", "Scrum", "Testing", "Debugging", "Documentation"]},
                    {"phase": 10, "title": "Projects", "duration": "6 Weeks", "learn": ["Calculator", "Student Grade System", "Hospital Management System", "Chat Application", "E-Commerce Backend"]},
                    {"phase": 11, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Project Documentation"]},
                    {"phase": 12, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Java/Python, OOP, SQL, DSA)", "HR (Tell Me About Yourself, Strengths)", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator", "Student Grade System", "Banking Console Application", "Library Management System", "Number Guessing Game"],
                    "Intermediate": ["Hospital Management System", "Employee Management System", "Inventory Management", "Chat Application", "Hotel Management System"],
                    "Advanced": ["E-Commerce Backend", "Learning Management System", "Online Examination Portal", "Job Portal", "ERP Mini System"]
                },
                "practice_questions": {
                    "Programming": ["100 Beginner", "100 Intermediate", "100 Advanced"],
                    "DSA": ["Arrays - 50", "Strings - 50", "Linked Lists - 40", "Trees - 60", "Graphs - 50", "Dynamic Programming - 40"]
                },
                "certifications": ["Oracle Java Foundations", "Python Programming Certification", "SQL Certification", "Git & GitHub Certification", "Software Engineering Fundamentals"],
                "readiness_checklist": ["Computer Fundamentals", "Programming Language", "Object-Oriented Programming", "SQL", "DBMS", "Operating Systems", "Computer Networks", "Data Structures", "Algorithms", "Git & GitHub", "500+ Coding Problems Solved", "10+ Projects Completed", "ATS Resume Created", "GitHub Portfolio Ready", "LinkedIn Profile Updated", "15 Mock Interviews Completed", "Ready for Software Engineer Interviews"]
            }
        )

        # ----------------------------------------------------------------
        # 2. Software Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Software Developer",
                "slug": "software-developer",
                "overview": "Career Category: Software Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–9 LPA, Mid-Level: ₹8–18 LPA, Senior: ₹20–45+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Adobe, Oracle, IBM, SAP, Infosys, TCS, Wipro, Cognizant, Accenture, Capgemini",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Software Developer Complete Roadmap",
                "description": "Your complete guide to becoming a successful Software Developer.",
                "skills_matrix": {
                    "Programming Languages": ["Java (Recommended)", "Python", "C Programming", "JavaScript", "C++ (Optional)"],
                    "Computer Science Fundamentals": ["Programming Logic", "OOP", "Data Structures", "Algorithms", "Operating Systems", "DBMS", "Computer Networks"],
                    "Frontend Basics": ["HTML5", "CSS3", "Bootstrap", "JavaScript"],
                    "Backend Development": ["Spring Boot (Java)", "Django/Flask (Python)", "REST APIs", "Authentication & Authorization"],
                    "Database": ["SQL", "MySQL", "PostgreSQL", "MongoDB (Basics)"],
                    "Version Control": ["Git", "GitHub"],
                    "Development Tools": ["Visual Studio Code", "IntelliJ IDEA", "Eclipse", "Postman"],
                    "Software Engineering": ["SDLC", "Agile", "Scrum", "Debugging", "Unit Testing", "API Testing"],
                    "Deployment Basics": ["Docker", "GitHub Actions (Basics)", "Vercel/Render"],
                    "Soft Skills": ["Problem Solving", "Communication", "Teamwork", "Critical Thinking", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Operating Systems", "Internet", "File Management", "SDLC Introduction"]},
                    {"phase": 2, "title": "Programming Fundamentals", "duration": "4 Weeks", "learn": ["Variables", "Data Types", "Operators", "Conditional Statements", "Loops", "Functions", "Arrays", "Strings", "Collections", "Exception Handling", "File Handling"]},
                    {"phase": 3, "title": "Object-Oriented Programming", "duration": "2 Weeks", "learn": ["Classes", "Objects", "Constructors", "Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "Interfaces"]},
                    {"phase": 4, "title": "Data Structures & Algorithms", "duration": "8 Weeks", "learn": ["Arrays", "Strings", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Hash Tables", "Searching", "Sorting", "Recursion", "Dynamic Programming", "Greedy Algorithms"]},
                    {"phase": 5, "title": "Database", "duration": "3 Weeks", "learn": ["SQL", "CRUD Operations", "Joins", "Aggregate Functions", "Views", "Indexes", "Transactions", "Stored Procedures"]},
                    {"phase": 6, "title": "Frontend Basics", "duration": "3 Weeks", "learn": ["HTML5", "CSS3", "Bootstrap", "JavaScript Basics"]},
                    {"phase": 7, "title": "Backend Development", "duration": "5 Weeks", "learn": ["Spring Boot OR Django/Flask", "REST APIs", "CRUD Operations", "Authentication", "Authorization", "JWT Basics"]},
                    {"phase": 8, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request", "Collaboration"]},
                    {"phase": 9, "title": "Software Development Process", "duration": "2 Weeks", "learn": ["SDLC", "Agile", "Scrum", "Debugging", "Unit Testing", "Integration Testing"]},
                    {"phase": 10, "title": "Full Software Projects", "duration": "6 Weeks", "learn": ["Calculator", "Student Grade Calculator", "Banking Console App", "Employee Management", "Quiz Application"]},
                    {"phase": 11, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Personal Portfolio Website"]},
                    {"phase": 12, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Programming, OOP, DSA, SQL, DBMS, OS, Networks, SDLC, REST)", "HR (Self Intro, Career Goals, Teamwork)", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator", "Student Grade Calculator", "Banking Console App", "Employee Management", "Quiz Application"],
                    "Intermediate": ["Library Management", "Hospital Management", "Inventory System", "Online Voting System", "Chat Application"],
                    "Advanced": ["E-Commerce System", "Job Portal", "Learning Management System", "CRM System", "ERP Mini Project"]
                },
                "practice_questions": {
                    "Programming": ["100 Beginner", "150 Intermediate", "150 Advanced"],
                    "SQL": ["100 SQL Queries"],
                    "DSA": ["Arrays - 50", "Strings - 50", "Linked Lists - 40", "Stack & Queue - 40", "Trees - 60", "Graphs - 50", "Dynamic Programming - 40"]
                },
                "certifications": ["Oracle Certified Professional Java", "Python Programming Certification", "SQL Certification", "Git & GitHub Certification", "Spring Boot Certification", "REST API Development", "Software Engineering Fundamentals"],
                "readiness_checklist": ["Computer Fundamentals", "Programming Language (Java/Python)", "Object-Oriented Programming", "HTML, CSS, JavaScript Basics", "SQL & Database Management", "Data Structures & Algorithms", "Operating Systems", "Computer Networks", "Backend Development", "REST API Development", "Git & GitHub", "Software Development Lifecycle", "600+ Coding Problems Solved", "10+ Software Projects Completed", "ATS Resume Created", "GitHub Portfolio Ready", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Software Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 3. Full Stack Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Full Stack Developer",
                "slug": "full-stack-developer",
                "overview": "Career Category: Web Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–10 LPA, Mid-Level: ₹10–20 LPA, Senior: ₹20–50+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Adobe, Flipkart, Swiggy, Zomato, Infosys, TCS, Cognizant, Accenture, Capgemini, IBM",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Full Stack Developer Complete Roadmap",
                "description": "Master both frontend and backend development to build complete web applications.",
                "skills_matrix": {
                    "Frontend Development": ["HTML5", "CSS3", "Bootstrap 5", "Tailwind CSS", "JavaScript (ES6+)", "TypeScript (Optional)", "React.js", "Next.js"],
                    "Backend Development": ["Node.js", "Express.js", "REST APIs", "Authentication (JWT)", "Authorization", "API Security"],
                    "Database": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Database Design"],
                    "Programming Languages": ["JavaScript", "TypeScript (Optional)", "Python (Optional)", "Java (Optional)"],
                    "Version Control": ["Git", "GitHub"],
                    "Deployment": ["Vercel", "Render", "Netlify", "Docker (Basics)"],
                    "Development Tools": ["Visual Studio Code", "Postman", "Chrome DevTools", "npm", "Git Bash"],
                    "Software Engineering": ["SDLC", "Agile", "Debugging", "Testing", "API Documentation"],
                    "Soft Skills": ["Communication", "Problem Solving", "Critical Thinking", "Teamwork", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Internet", "File Management", "VS Code Installation", "Git Installation"]},
                    {"phase": 2, "title": "HTML5", "duration": "1 Week", "learn": ["HTML Structure", "Semantic Tags", "Forms", "Tables", "Multimedia", "SEO Basics"]},
                    {"phase": 3, "title": "CSS3", "duration": "2 Weeks", "learn": ["Selectors", "Colors", "Box Model", "Flexbox", "CSS Grid", "Animations", "Responsive Design"]},
                    {"phase": 4, "title": "Bootstrap & Tailwind CSS", "duration": "2 Weeks", "learn": ["Bootstrap Components", "Grid System", "Tailwind Utility Classes", "Responsive Layouts"]},
                    {"phase": 5, "title": "JavaScript", "duration": "5 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "Objects", "DOM Manipulation", "Events", "ES6+", "Fetch API", "Async/Await", "Promises"]},
                    {"phase": 6, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request", "Collaboration"]},
                    {"phase": 7, "title": "React.js", "duration": "5 Weeks", "learn": ["Components", "JSX", "Props", "State", "Hooks", "Routing", "Forms", "Context API", "API Integration"]},
                    {"phase": 8, "title": "Next.js", "duration": "2 Weeks", "learn": ["Routing", "Server Components", "Client Components", "API Routes", "Deployment"]},
                    {"phase": 9, "title": "Backend Development", "duration": "5 Weeks", "learn": ["Node.js", "Express.js", "REST APIs", "CRUD Operations", "Authentication", "Authorization", "JWT", "File Upload"]},
                    {"phase": 10, "title": "Database", "duration": "3 Weeks", "learn": ["MongoDB", "MySQL", "SQL Queries", "Database Relationships", "Mongoose ORM"]},
                    {"phase": 11, "title": "Full Stack Development", "duration": "5 Weeks", "learn": ["Frontend + Backend Integration", "Authentication", "Authorization", "API Integration", "Deployment"]},
                    {"phase": 12, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Postman", "Debugging", "Error Handling", "Docker Basics", "Deploy to Vercel", "Deploy Backend to Render"]},
                    {"phase": 13, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Portfolio Website"]},
                    {"phase": 14, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (HTML, CSS, JS, React, Next, Node, Express, MongoDB, SQL, REST APIs)", "HR (Tell Me About Yourself, Project Explanation)", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Personal Portfolio", "Calculator", "Todo App", "Weather App", "Digital Clock"],
                    "Intermediate": ["Expense Tracker", "Movie Search App", "Notes App", "Blog Website", "Employee Management System"],
                    "Advanced": ["E-Commerce Website", "Learning Management System", "Hospital Management System", "Job Portal", "Social Media Application"],
                    "Industry-Level": ["Online Banking System", "Food Delivery Platform", "Real-Time Chat Application", "Online Examination System", "College ERP Management System"]
                },
                "practice_questions": {
                    "HTML": ["20 Practice Exercises"],
                    "CSS": ["40 Layout Challenges"],
                    "JavaScript": ["200 Coding Problems"],
                    "React.js": ["50 Component Challenges"],
                    "Node.js": ["50 API Challenges"],
                    "SQL": ["100 SQL Queries"],
                    "MongoDB": ["50 Database Exercises"]
                },
                "certifications": ["Responsive Web Design", "JavaScript Certification", "React Developer Certification", "Node.js Certification", "MongoDB Certification", "SQL Certification", "Git & GitHub Certification", "Full Stack Web Development Certification"],
                "readiness_checklist": ["HTML5", "CSS3", "Bootstrap", "Tailwind CSS", "JavaScript (ES6+)", "Git & GitHub", "React.js", "Next.js", "Node.js", "Express.js", "REST APIs", "Authentication (JWT)", "SQL", "MongoDB", "Deployment", "Debugging", "700+ Practice Problems Solved", "15+ Real-World Projects Completed", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Full Stack Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 4. Frontend Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Frontend Developer",
                "slug": "frontend-developer",
                "overview": "Career Category: Web Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–8 LPA, Mid-Level: ₹8–18 LPA, Senior: ₹18–40+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Adobe, Flipkart, Swiggy, Zomato, Infosys, TCS, Cognizant, Accenture, Capgemini, IBM",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Frontend Developer Complete Roadmap",
                "description": "Master the art of building responsive and interactive user interfaces for modern web applications.",
                "skills_matrix": {
                    "Core Web Technologies": ["HTML5", "CSS3", "Responsive Web Design", "JavaScript (ES6+)", "TypeScript (Optional)"],
                    "CSS Frameworks": ["Bootstrap 5", "Tailwind CSS", "Material UI"],
                    "JavaScript Frameworks/Libraries": ["React.js", "Next.js", "Redux Toolkit", "React Router"],
                    "UI/UX Skills": ["Responsive Design", "Mobile-First Design", "Wireframing Basics", "Accessibility (WCAG)", "Cross-Browser Compatibility"],
                    "Version Control": ["Git", "GitHub"],
                    "API Integration": ["REST APIs", "JSON", "Fetch API", "Axios"],
                    "Development Tools": ["Visual Studio Code", "Chrome DevTools", "Postman", "npm", "Vite"],
                    "Deployment": ["GitHub Pages", "Netlify", "Vercel"],
                    "Soft Skills": ["Problem Solving", "Communication", "Creativity", "Teamwork", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Internet", "VS Code Installation", "Browser Developer Tools", "Git Installation"]},
                    {"phase": 2, "title": "HTML5", "duration": "2 Weeks", "learn": ["HTML Structure", "Semantic Elements", "Forms", "Tables", "Multimedia", "SEO Basics"]},
                    {"phase": 3, "title": "CSS3", "duration": "3 Weeks", "learn": ["Selectors", "Colors", "Typography", "Box Model", "Flexbox", "CSS Grid", "Animations", "Transitions", "Responsive Design"]},
                    {"phase": 4, "title": "Bootstrap & Tailwind CSS", "duration": "2 Weeks", "learn": ["Bootstrap Components", "Bootstrap Grid", "Tailwind Utility Classes", "Responsive Layouts", "Material UI Basics"]},
                    {"phase": 5, "title": "JavaScript", "duration": "5 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "Objects", "DOM Manipulation", "Events", "ES6+", "Promises", "Async/Await", "Fetch API"]},
                    {"phase": 6, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Push", "Pull", "Branch", "Merge", "Pull Requests"]},
                    {"phase": 7, "title": "React.js", "duration": "5 Weeks", "learn": ["JSX", "Components", "Props", "State", "Hooks", "Routing", "Forms", "Context API", "API Integration"]},
                    {"phase": 8, "title": "Redux Toolkit", "duration": "2 Weeks", "learn": ["Store", "Slice", "Actions", "Reducers", "Async Thunk"]},
                    {"phase": 9, "title": "Next.js", "duration": "2 Weeks", "learn": ["Routing", "Layouts", "Server Components", "Client Components", "SEO", "Deployment"]},
                    {"phase": 10, "title": "API Integration", "duration": "2 Weeks", "learn": ["REST APIs", "JSON", "Fetch API", "Axios", "Authentication Basics"]},
                    {"phase": 11, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Debugging", "Browser DevTools", "Performance Optimization", "Lighthouse", "Netlify", "Vercel"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Personal Portfolio Website"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (HTML, CSS, Bootstrap, Tailwind, JS, React, Redux, Next, APIs)", "HR (Tell Me About Yourself, Project Explanation)", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Personal Portfolio", "Resume Website", "Calculator", "Digital Clock", "Landing Page"],
                    "Intermediate": ["Weather App", "Movie Search App", "Expense Tracker", "Notes App", "Quiz Application"],
                    "Advanced": ["E-Commerce Frontend", "Learning Management Dashboard", "Job Portal Frontend", "Social Media UI", "Admin Dashboard"],
                    "Industry-Level": ["Netflix Clone", "Amazon Clone", "Food Delivery Website", "Banking Dashboard", "Hospital Management Frontend"]
                },
                "practice_questions": {
                    "HTML": ["30 Practice Exercises"],
                    "CSS": ["50 Layout Challenges"],
                    "JavaScript": ["250 Coding Problems"],
                    "React.js": ["60 Component Challenges"],
                    "Redux Toolkit": ["25 State Management Exercises"],
                    "API Integration": ["30 REST API Challenges"]
                },
                "certifications": ["HTML & CSS Certification", "Responsive Web Design Certification", "JavaScript Certification", "React Developer Certification", "Next.js Certification", "Git & GitHub Certification", "Frontend Web Development Certification"],
                "readiness_checklist": ["HTML5", "CSS3", "Responsive Web Design", "Bootstrap 5", "Tailwind CSS", "JavaScript (ES6+)", "Git & GitHub", "React.js", "Redux Toolkit", "Next.js", "REST API Integration", "Browser Debugging", "Website Deployment", "700+ Practice Problems Solved", "15+ Frontend Projects Completed", "Portfolio Website Ready", "GitHub Portfolio Updated", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Frontend Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 5. Backend Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Backend Developer",
                "slug": "backend-developer",
                "overview": "Career Category: Software Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–10 LPA, Mid-Level: ₹10–22 LPA, Senior: ₹20–60+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Adobe, Oracle, IBM, SAP, Flipkart, Swiggy, Zomato, Infosys, TCS, Cognizant, Accenture, Capgemini",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Backend Developer Complete Roadmap",
                "description": "Master the art of building scalable and secure server-side applications and APIs.",
                "skills_matrix": {
                    "Programming Languages": ["Java (Recommended)", "Python", "JavaScript (Node.js)", "C++ (Optional)", "Go (Optional)"],
                    "Backend Frameworks": ["Spring Boot (Java)", "Node.js", "Express.js", "Django", "Flask", "FastAPI"],
                    "Database": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis (Caching)"],
                    "API Development": ["REST APIs", "GraphQL (Basics)", "API Documentation (Swagger/OpenAPI)", "JSON"],
                    "Authentication & Security": ["JWT Authentication", "OAuth 2.0", "Session Management", "Password Hashing (bcrypt)", "Role-Based Access Control (RBAC)", "CORS", "HTTPS", "API Security"],
                    "Version Control": ["Git", "GitHub"],
                    "Testing": ["Unit Testing", "Integration Testing", "Postman", "JUnit / PyTest"],
                    "Deployment & DevOps": ["Docker", "Nginx", "Linux Basics", "CI/CD (GitHub Actions)", "AWS/Render/Railway (Basics)"],
                    "Software Engineering": ["SDLC", "Agile", "Design Patterns", "MVC Architecture", "Clean Code Principles"],
                    "Soft Skills": ["Problem Solving", "Logical Thinking", "Communication", "Team Collaboration", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Operating Systems", "Linux Basics", "Internet", "Development Environment Setup"]},
                    {"phase": 2, "title": "Programming Fundamentals", "duration": "4 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "Strings", "Collections", "Exception Handling", "File Handling"]},
                    {"phase": 3, "title": "Object-Oriented Programming", "duration": "2 Weeks", "learn": ["Classes", "Objects", "Constructors", "Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "Interfaces"]},
                    {"phase": 4, "title": "Data Structures & Algorithms", "duration": "8 Weeks", "learn": ["Arrays", "Strings", "Linked Lists", "Stack", "Queue", "Trees", "Graphs", "Hash Tables", "Searching", "Sorting", "Recursion", "Dynamic Programming"]},
                    {"phase": 5, "title": "Database Management", "duration": "3 Weeks", "learn": ["SQL", "CRUD Operations", "Joins", "Stored Procedures", "Views", "Transactions", "Indexing", "Database Design", "Normalization", "MongoDB Basics"]},
                    {"phase": 6, "title": "Backend Framework", "duration": "6 Weeks", "learn": ["Spring Boot OR Django OR Node.js/Express"]},
                    {"phase": 7, "title": "API Development", "duration": "3 Weeks", "learn": ["REST APIs", "CRUD APIs", "JSON", "HTTP Methods", "Status Codes", "API Documentation", "Swagger"]},
                    {"phase": 8, "title": "Authentication & Authorization", "duration": "2 Weeks", "learn": ["JWT", "OAuth Basics", "Login System", "Registration", "Password Encryption", "RBAC"]},
                    {"phase": 9, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request", "Collaboration"]},
                    {"phase": 10, "title": "Deployment & DevOps", "duration": "3 Weeks", "learn": ["Linux Commands", "Docker", "Nginx", "CI/CD Basics", "GitHub Actions", "Cloud Deployment (Render/AWS)"]},
                    {"phase": 11, "title": "Full Backend Projects", "duration": "6 Weeks", "learn": ["Student Management API", "Hospital Management Backend", "E-Commerce Backend", "Learning Management System Backend", "Job Portal Backend"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "API Documentation", "Project Documentation"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Programming, OOP, DSA, SQL, DBMS, OS, Networks, Backend Frameworks, REST APIs)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Student Management API", "Notes API", "Calculator API", "Contact Management API", "Employee API"],
                    "Intermediate": ["Library Management Backend", "Hospital Management Backend", "Banking Backend", "Blog API", "Inventory Management Backend"],
                    "Advanced": ["E-Commerce Backend", "Job Portal Backend", "Food Delivery Backend", "Learning Management Backend", "Social Media Backend"],
                    "Industry-Level": ["Digital Banking Platform", "Ride Booking Backend", "Video Streaming Backend", "Cloud File Storage API", "College ERP Backend"]
                },
                "practice_questions": {
                    "Programming": ["150 Beginner", "150 Intermediate", "150 Advanced"],
                    "SQL": ["150 SQL Queries"],
                    "REST API": ["50 API Development Exercises"],
                    "MongoDB": ["50 Database Exercises"],
                    "Authentication": ["25 Security Challenges"]
                },
                "certifications": ["Java Spring Boot Certification", "Python Django Certification", "Node.js Certification", "REST API Development Certification", "SQL Certification", "MongoDB Certification", "Docker Certification", "Git & GitHub Certification", "Backend Development Certification"],
                "readiness_checklist": ["Programming Language (Java/Python/JavaScript)", "Object-Oriented Programming", "Data Structures & Algorithms", "SQL & Database Design", "MongoDB", "Spring Boot / Django / Node.js", "REST API Development", "JWT Authentication", "OAuth Basics", "Git & GitHub", "Docker", "Linux Basics", "API Documentation (Swagger)", "Cloud Deployment", "800+ Practice Problems Solved", "15+ Backend Projects Completed", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Backend Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 6. Web Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Web Developer",
                "slug": "web-developer",
                "overview": "Career Category: Web Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–8 LPA, Mid-Level: ₹8–18 LPA, Senior: ₹18–40+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Adobe, IBM, Infosys, TCS, Wipro, Cognizant, Accenture, Capgemini, Zoho, Freshworks",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Web Developer Complete Roadmap",
                "description": "Learn the essential skills to build responsive, user-friendly, and interactive websites.",
                "skills_matrix": {
                    "Core Web Technologies": ["HTML5", "CSS3", "JavaScript (ES6+)"],
                    "CSS Frameworks": ["Bootstrap 5", "Tailwind CSS"],
                    "Frontend Libraries": ["React.js", "Next.js (Recommended)"],
                    "Backend Technologies": ["Node.js", "Express.js", "Django (Python)", "Flask (Optional)"],
                    "Database": ["MySQL", "PostgreSQL", "MongoDB"],
                    "API Development": ["REST APIs", "JSON", "Fetch API", "Axios"],
                    "Version Control": ["Git", "GitHub"],
                    "Deployment": ["GitHub Pages", "Netlify", "Vercel", "Render"],
                    "Development Tools": ["Visual Studio Code", "Chrome DevTools", "Postman", "npm"],
                    "Web Concepts": ["Responsive Design", "SEO Basics", "Accessibility (WCAG)", "Authentication (JWT)", "Web Security Basics"],
                    "Soft Skills": ["Problem Solving", "Communication", "Creativity", "Teamwork", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer Fundamentals", "duration": "1 Week", "learn": ["Computer Basics", "Internet", "File Management", "VS Code Installation", "Browser Developer Tools"]},
                    {"phase": 2, "title": "HTML5", "duration": "2 Weeks", "learn": ["HTML Structure", "Semantic HTML", "Forms", "Tables", "Multimedia", "SEO Basics"]},
                    {"phase": 3, "title": "CSS3", "duration": "3 Weeks", "learn": ["Selectors", "Box Model", "Flexbox", "CSS Grid", "Typography", "Animations", "Responsive Design"]},
                    {"phase": 4, "title": "Bootstrap & Tailwind CSS", "duration": "2 Weeks", "learn": ["Bootstrap Components", "Grid System", "Tailwind Utility Classes", "Responsive Layouts"]},
                    {"phase": 5, "title": "JavaScript", "duration": "5 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "Objects", "DOM Manipulation", "Events", "ES6+", "Promises", "Async/Await", "Fetch API"]},
                    {"phase": 6, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Requests"]},
                    {"phase": 7, "title": "React.js", "duration": "5 Weeks", "learn": ["JSX", "Components", "Props", "State", "Hooks", "Routing", "Forms", "Context API"]},
                    {"phase": 8, "title": "Backend Development", "duration": "5 Weeks", "learn": ["Node.js", "Express.js", "REST APIs", "CRUD Operations", "Authentication (JWT)", "Authorization"]},
                    {"phase": 9, "title": "Database", "duration": "3 Weeks", "learn": ["SQL", "MySQL", "MongoDB", "Database Relationships", "Mongoose ORM"]},
                    {"phase": 10, "title": "Full Stack Integration", "duration": "4 Weeks", "learn": ["Frontend + Backend Integration", "API Integration", "Authentication Flow", "Deployment"]},
                    {"phase": 11, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Chrome DevTools", "Debugging", "Performance Optimization", "Lighthouse", "Deployment (Netlify, Vercel, Render)"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Personal Portfolio Website"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (HTML, CSS, JS, React, Node, SQL, MongoDB, REST APIs, Security, Design)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Portfolio Website", "Calculator", "Digital Clock", "Landing Page", "To-Do List"],
                    "Intermediate": ["Weather App", "Expense Tracker", "Blog Website", "Quiz Application", "Employee Management System"],
                    "Advanced": ["E-Commerce Website", "Learning Management System", "Job Portal", "Social Media Platform", "Hospital Management System"],
                    "Industry-Level": ["Online Banking Website", "Food Delivery Platform", "Video Streaming Platform", "College ERP System", "Real-Time Chat Application"]
                },
                "practice_questions": {
                    "HTML": ["30 Exercises"],
                    "CSS": ["50 Responsive Layout Challenges"],
                    "JavaScript": ["250 Coding Problems"],
                    "React.js": ["60 Component Challenges"],
                    "SQL": ["100 SQL Queries"],
                    "REST APIs": ["50 API Integration Challenges"],
                    "MongoDB": ["50 Database Exercises"]
                },
                "certifications": ["HTML & CSS Certification", "JavaScript Certification", "React Developer Certification", "Node.js Certification", "MongoDB Certification", "SQL Certification", "Git & GitHub Certification", "Full Stack Web Development Certification"],
                "readiness_checklist": ["HTML5", "CSS3", "Bootstrap 5", "Tailwind CSS", "JavaScript (ES6+)", "React.js", "Node.js", "Express.js", "SQL", "MongoDB", "REST API Development", "Authentication (JWT)", "Git & GitHub", "Deployment", "Responsive Web Design", "Web Security Basics", "800+ Practice Problems Solved", "15+ Web Development Projects Completed", "Portfolio Website Ready", "GitHub Portfolio Updated", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Web Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 7. Mobile App Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Mobile App Developer",
                "slug": "mobile-app-developer",
                "overview": "Career Category: Mobile Application Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–10 LPA, Mid-Level: ₹10–20 LPA, Senior: ₹20–50+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Microsoft, Amazon, Flipkart, PhonePe, Razorpay, Swiggy, Zomato, Paytm, Samsung, Infosys, TCS, Cognizant, Accenture",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Mobile App Developer Complete Roadmap",
                "description": "Master mobile application development and build cross-platform or native apps.",
                "skills_matrix": {
                    "Programming Languages": ["Dart (Flutter)", "Kotlin (Android)", "Java (Android)", "Swift (iOS - Optional)", "JavaScript (React Native - Optional)"],
                    "Mobile Frameworks": ["Flutter (Recommended)", "React Native", "Android SDK", "Jetpack Compose", "SwiftUI (Optional)"],
                    "UI Development": ["Material Design", "Cupertino Widgets", "Responsive Mobile UI", "Animations", "State Management"],
                    "Backend Integration": ["REST APIs", "GraphQL (Basics)", "JSON", "Firebase"],
                    "Database": ["SQLite", "Hive", "Shared Preferences", "Firebase Firestore", "MySQL (Backend)"],
                    "Authentication": ["Firebase Authentication", "JWT", "Google Sign-In", "OTP Login", "Social Login"],
                    "Version Control": ["Git", "GitHub"],
                    "Development Tools": ["Android Studio", "Visual Studio Code", "Xcode (Mac)", "Postman", "Firebase Console"],
                    "Deployment": ["Google Play Console", "Apple App Store Connect", "Firebase App Distribution"],
                    "Software Engineering": ["SDLC", "Agile", "MVC/MVVM Architecture", "Clean Architecture", "Debugging", "Testing"],
                    "Soft Skills": ["Problem Solving", "Communication", "UI/UX Understanding", "Time Management", "Team Collaboration"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Computer & Programming Fundamentals", "duration": "2 Weeks", "learn": ["Computer Basics", "Programming Logic", "Variables", "Data Types", "Loops", "Functions", "OOP Concepts"]},
                    {"phase": 2, "title": "Dart Programming", "duration": "3 Weeks", "learn": ["Variables", "Functions", "Classes", "Collections", "Async Programming", "Exception Handling", "OOP"]},
                    {"phase": 3, "title": "Flutter Basics", "duration": "4 Weeks", "learn": ["Flutter Installation", "Widgets", "Layouts", "Navigation", "Forms", "Themes", "Assets", "Responsive Design"]},
                    {"phase": 4, "title": "State Management", "duration": "2 Weeks", "learn": ["Provider", "Riverpod", "Bloc (Basics)", "GetX (Optional)"]},
                    {"phase": 5, "title": "API Integration", "duration": "2 Weeks", "learn": ["REST APIs", "HTTP Package", "JSON Parsing", "Error Handling"]},
                    {"phase": 6, "title": "Database", "duration": "3 Weeks", "learn": ["SQLite", "Hive", "Shared Preferences", "Firebase Firestore"]},
                    {"phase": 7, "title": "Firebase", "duration": "3 Weeks", "learn": ["Authentication", "Firestore", "Storage", "Push Notifications", "Analytics"]},
                    {"phase": 8, "title": "Mobile Architecture", "duration": "2 Weeks", "learn": ["MVVM", "Clean Architecture", "Repository Pattern", "Dependency Injection"]},
                    {"phase": 9, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request"]},
                    {"phase": 10, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Unit Testing", "Widget Testing", "Debugging", "Performance Optimization", "APK Build", "Play Store Publishing"]},
                    {"phase": 11, "title": "Advanced Mobile Development", "duration": "5 Weeks", "learn": ["Offline Storage", "Payment Gateway Integration", "Maps Integration", "Camera", "Location Services", "Background Services", "Push Notifications", "Deep Linking"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Play Store Portfolio"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Dart, Flutter, State Management, Firebase, REST APIs, SQLite, OOP, Architecture)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator App", "To-Do App", "Notes App", "BMI Calculator", "Digital Clock"],
                    "Intermediate": ["Weather App", "Expense Tracker", "Quiz App", "Music Player", "News Application"],
                    "Advanced": ["E-Commerce App", "Food Delivery App", "Hospital Management App", "Learning Management App", "Job Portal App"],
                    "Industry-Level": ["Banking Application", "Ride Booking App", "Video Streaming App", "Social Media App", "College ERP Mobile App"]
                },
                "practice_questions": {
                    "Dart Programming": ["150 Coding Problems"],
                    "Flutter Widgets": ["100 UI Challenges"],
                    "API Integration": ["50 REST API Exercises"],
                    "Firebase": ["50 Authentication & Firestore Tasks"],
                    "Database": ["50 SQLite/Hive Exercises"],
                    "State Management": ["50 Provider/Riverpod Challenges"]
                },
                "certifications": ["Flutter Development Certification", "Dart Programming Certification", "Firebase Certification", "Android Development Certification", "React Native Certification (Optional)", "Git & GitHub Certification", "Mobile App Development Certification"],
                "readiness_checklist": ["Programming Fundamentals", "Dart Programming", "Flutter Framework", "Responsive Mobile UI", "State Management", "REST API Integration", "Firebase Authentication", "Firestore Database", "SQLite/Hive", "Git & GitHub", "Mobile App Architecture", "Testing & Debugging", "Google Play Store Deployment", "700+ Practice Problems Solved", "15+ Mobile Applications Developed", "GitHub Portfolio Ready", "Play Store Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Mobile App Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 8. Android Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Android Developer",
                "slug": "android-developer",
                "overview": "Career Category: Mobile Application Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–10 LPA, Mid-Level: ₹10–22 LPA, Senior: ₹22–50+ LPA",
                "industry_demand": "High. Top Recruiters: Google, Samsung, Microsoft, Amazon, PhonePe, Paytm, Flipkart, Swiggy, Zomato, Razorpay, Infosys, TCS, Cognizant, Accenture",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Android Developer Complete Roadmap",
                "description": "Master Android app development using Kotlin, Android Studio, and modern architecture.",
                "skills_matrix": {
                    "Programming Languages": ["Kotlin (Recommended)", "Java", "XML (Android UI)", "SQL"],
                    "Android Development": ["Android SDK", "Android Studio", "Jetpack Compose", "Android Jetpack Libraries", "Material Design"],
                    "Android Components": ["Activities", "Fragments", "Intents", "Services", "Broadcast Receivers", "Content Providers"],
                    "Architecture": ["MVVM", "Clean Architecture", "Repository Pattern", "Dependency Injection (Hilt)"],
                    "State & Data Management": ["ViewModel", "LiveData", "StateFlow", "Room Database", "DataStore", "Shared Preferences"],
                    "Networking": ["REST APIs", "Retrofit", "OkHttp", "JSON Parsing"],
                    "Firebase": ["Authentication", "Firestore", "Realtime Database", "Cloud Storage", "Push Notifications", "Analytics", "Crashlytics"],
                    "Version Control": ["Git", "GitHub"],
                    "Testing": ["JUnit", "Espresso", "Mockito", "Debugging"],
                    "Deployment": ["Google Play Console", "App Signing", "Play Store Publishing"],
                    "Soft Skills": ["Problem Solving", "Communication", "UI/UX Understanding", "Teamwork", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Programming Fundamentals", "duration": "3 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "OOP Concepts", "Exception Handling"]},
                    {"phase": 2, "title": "Kotlin Programming", "duration": "3 Weeks", "learn": ["Classes", "Objects", "Collections", "Lambdas", "Coroutines", "Null Safety", "Extensions"]},
                    {"phase": 3, "title": "Android Basics", "duration": "4 Weeks", "learn": ["Android Studio", "Project Structure", "Activities", "Intents", "Fragments", "XML Layouts", "Material Components"]},
                    {"phase": 4, "title": "Jetpack Compose", "duration": "3 Weeks", "learn": ["Compose UI", "Layouts", "Navigation", "State Management", "Material 3", "Animations"]},
                    {"phase": 5, "title": "Android Architecture", "duration": "3 Weeks", "learn": ["MVVM", "ViewModel", "LiveData", "StateFlow", "Repository Pattern", "Hilt Dependency Injection"]},
                    {"phase": 6, "title": "Database", "duration": "3 Weeks", "learn": ["Room Database", "SQLite Basics", "Shared Preferences", "DataStore"]},
                    {"phase": 7, "title": "API Integration", "duration": "3 Weeks", "learn": ["Retrofit", "OkHttp", "REST APIs", "JSON", "Error Handling"]},
                    {"phase": 8, "title": "Firebase", "duration": "3 Weeks", "learn": ["Authentication", "Firestore", "Storage", "Push Notifications", "Crashlytics", "Analytics"]},
                    {"phase": 9, "title": "Advanced Android Features", "duration": "4 Weeks", "learn": ["Camera API", "Google Maps", "GPS & Location", "Background Services", "WorkManager", "Deep Linking", "Payment Gateway Integration"]},
                    {"phase": 10, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Branch", "Merge", "Pull Request"]},
                    {"phase": 11, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Unit Testing", "UI Testing", "Debugging", "APK Generation", "App Bundle", "Google Play Publishing"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Google Play Developer Portfolio"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Kotlin, Android SDK, Compose, MVVM, Room, REST APIs, Firebase)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator App", "BMI Calculator", "Notes App", "To-Do App", "Digital Clock"],
                    "Intermediate": ["Weather App", "Expense Tracker", "Quiz App", "Music Player", "News App"],
                    "Advanced": ["E-Commerce App", "Food Delivery App", "Banking App", "Hospital Management App", "Learning Management App"],
                    "Industry-Level": ["Ride Booking App", "Social Media App", "Video Streaming App", "Job Portal App", "College ERP Mobile App"]
                },
                "practice_questions": {
                    "Kotlin": ["200 Programming Problems"],
                    "Android UI": ["100 UI Challenges"],
                    "Jetpack Compose": ["50 Compose Exercises"],
                    "REST APIs": ["50 API Integration Tasks"],
                    "Firebase": ["50 Authentication & Firestore Exercises"],
                    "Room Database": ["50 Database Challenges"]
                },
                "certifications": ["Android Developer Certification", "Kotlin Programming Certification", "Android Jetpack Compose Certification", "Firebase Certification", "Google Associate Android Developer (if available)", "Git & GitHub Certification", "Mobile Application Development Certification"],
                "readiness_checklist": ["Kotlin Programming", "Java Basics", "Android SDK", "Android Studio", "XML Layouts", "Jetpack Compose", "MVVM Architecture", "Room Database", "REST API Integration", "Firebase Authentication", "Firebase Firestore", "Git & GitHub", "Google Play Store Deployment", "800+ Practice Problems Solved", "15+ Android Applications Developed", "GitHub Portfolio Ready", "Play Store Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Android Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 9. iOS Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "iOS Developer",
                "slug": "ios-developer",
                "overview": "Career Category: Mobile Application Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹6–12 LPA, Mid-Level: ₹12–25 LPA, Senior: ₹25–60+ LPA",
                "industry_demand": "High. Top Recruiters: Apple, Google, Microsoft, Amazon, Adobe, Uber, Airbnb, Flipkart, PhonePe, Razorpay, Infosys, TCS, Cognizant, Accenture",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "iOS Developer Complete Roadmap",
                "description": "Master iOS app development using Swift, SwiftUI, and modern architecture.",
                "skills_matrix": {
                    "Programming Languages": ["Swift (Recommended)", "Objective-C (Basics)", "SQL"],
                    "iOS Development": ["Xcode", "SwiftUI", "UIKit", "Interface Builder", "Storyboards", "Auto Layout"],
                    "iOS Frameworks": ["Foundation", "UIKit", "SwiftUI", "Combine", "Core Data", "Core Location", "AVFoundation", "MapKit"],
                    "Architecture": ["MVC", "MVVM", "VIPER (Basics)", "Clean Architecture"],
                    "Data Storage": ["Core Data", "UserDefaults", "SQLite", "Realm Database", "Keychain"],
                    "Networking": ["REST APIs", "URLSession", "Alamofire", "JSON Parsing"],
                    "Authentication": ["Firebase Authentication", "Apple Sign-In", "Google Sign-In", "OAuth 2.0", "JWT"],
                    "Firebase": ["Firestore", "Cloud Storage", "Push Notifications", "Analytics", "Crashlytics"],
                    "Version Control": ["Git", "GitHub"],
                    "Testing": ["XCTest", "Unit Testing", "UI Testing", "Debugging"],
                    "Deployment": ["Apple Developer Program", "TestFlight", "App Store Connect", "App Store Publishing"],
                    "Soft Skills": ["Problem Solving", "Communication", "UI/UX Design Understanding", "Team Collaboration", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Programming Fundamentals", "duration": "3 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "OOP Concepts", "Exception Handling"]},
                    {"phase": 2, "title": "Swift Programming", "duration": "3 Weeks", "learn": ["Classes", "Structures", "Protocols", "Extensions", "Optionals", "Closures", "Error Handling", "Generics"]},
                    {"phase": 3, "title": "Xcode & UIKit", "duration": "4 Weeks", "learn": ["Xcode IDE", "Storyboards", "Auto Layout", "Navigation Controllers", "Table Views", "Collection Views"]},
                    {"phase": 4, "title": "SwiftUI", "duration": "3 Weeks", "learn": ["SwiftUI Views", "Layouts", "Navigation", "State Management", "Animations", "Lists", "Forms"]},
                    {"phase": 5, "title": "iOS Architecture", "duration": "3 Weeks", "learn": ["MVC", "MVVM", "Dependency Injection", "Combine Framework", "Clean Architecture"]},
                    {"phase": 6, "title": "Database", "duration": "3 Weeks", "learn": ["Core Data", "SQLite", "Realm", "UserDefaults", "Keychain"]},
                    {"phase": 7, "title": "Networking", "duration": "3 Weeks", "learn": ["REST APIs", "URLSession", "Alamofire", "JSON Parsing", "Error Handling"]},
                    {"phase": 8, "title": "Firebase", "duration": "3 Weeks", "learn": ["Authentication", "Firestore", "Storage", "Push Notifications", "Crashlytics", "Analytics"]},
                    {"phase": 9, "title": "Advanced iOS Features", "duration": "4 Weeks", "learn": ["Core Location", "MapKit", "Camera", "Face ID & Touch ID", "Apple Pay", "Background Tasks", "Deep Linking", "Push Notifications"]},
                    {"phase": 10, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request"]},
                    {"phase": 11, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["XCTest", "UI Testing", "Debugging", "Performance Optimization", "TestFlight", "App Store Deployment"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "App Store Portfolio"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Swift, SwiftUI, UIKit, MVVM, Core Data, REST APIs, Firebase, Combine)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator App", "Notes App", "BMI Calculator", "To-Do App", "Digital Clock"],
                    "Intermediate": ["Weather App", "Expense Tracker", "Quiz App", "Music Player", "News Application"],
                    "Advanced": ["E-Commerce App", "Food Delivery App", "Banking App", "Hospital Management App", "Learning Management App"],
                    "Industry-Level": ["Ride Booking App", "Social Media App", "Video Streaming App", "Job Portal App", "College ERP Mobile App"]
                },
                "practice_questions": {
                    "Swift Programming": ["200 Coding Problems"],
                    "SwiftUI": ["100 UI Challenges"],
                    "UIKit": ["50 Interface Challenges"],
                    "REST APIs": ["50 Networking Exercises"],
                    "Firebase": ["50 Authentication & Firestore Tasks"],
                    "Core Data": ["50 Database Exercises"]
                },
                "certifications": ["Swift Programming Certification", "iOS App Development Certification", "SwiftUI Certification", "UIKit Certification", "Firebase Certification", "Git & GitHub Certification", "Apple App Development Certification"],
                "readiness_checklist": ["Swift Programming", "Objective-C Basics", "Xcode", "UIKit", "SwiftUI", "MVVM Architecture", "Core Data", "REST API Integration", "Firebase Authentication", "Firebase Firestore", "Git & GitHub", "TestFlight Deployment", "Apple App Store Publishing", "800+ Practice Problems Solved", "15+ iOS Applications Developed", "GitHub Portfolio Ready", "App Store Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for iOS Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 10. Desktop Application Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Desktop Application Developer",
                "slug": "desktop-application-developer",
                "overview": "Career Category: Software Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–9 LPA, Mid-Level: ₹9–18 LPA, Senior: ₹18–40+ LPA",
                "industry_demand": "High. Top Recruiters: Microsoft, Oracle, SAP, Siemens, Autodesk, IBM, Dell, HP, Zoho, Freshworks, Infosys, TCS, Cognizant, Accenture, Capgemini",
                "who_can_apply": ", ".join(branches)
            },
            {
                "title": "Desktop Application Developer Complete Roadmap",
                "description": "Master desktop application development for Windows, macOS, or cross-platform using modern frameworks.",
                "skills_matrix": {
                    "Programming Languages": ["C# (Recommended)", "Java", "Python", "C++", "SQL"],
                    "Desktop Frameworks": [".NET / .NET Core / WinForms / WPF", "Java Swing / JavaFX", "Tkinter / PyQt5 / PySide6", "Qt Framework"],
                    "Database": ["MySQL", "PostgreSQL", "SQLite", "SQL Server"],
                    "UI Development": ["UI Design Principles", "Responsive Desktop Layouts", "Event Handling", "Data Binding", "Charts & Reports"],
                    "Software Engineering": ["Object-Oriented Programming", "Design Patterns", "MVC/MVVM", "SOLID Principles", "SDLC", "Agile"],
                    "File Handling": ["CSV", "Excel", "PDF", "JSON", "XML"],
                    "Networking": ["REST APIs", "HTTP Requests", "Socket Programming (Basics)"],
                    "Version Control": ["Git", "GitHub"],
                    "Testing": ["Unit Testing", "Debugging", "Logging", "Exception Handling"],
                    "Deployment": ["MSI Installer", "ClickOnce", "Inno Setup", "Microsoft Store (Optional)"],
                    "Development Tools": ["Visual Studio", "Visual Studio Code", "IntelliJ IDEA", "Eclipse", "PyCharm", "Qt Creator"],
                    "Soft Skills": ["Problem Solving", "Communication", "Team Collaboration", "Time Management", "Documentation"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Programming Fundamentals", "duration": "4 Weeks", "learn": ["Variables", "Data Types", "Operators", "Loops", "Functions", "Arrays", "OOP Concepts", "Exception Handling"]},
                    {"phase": 2, "title": "Object-Oriented Programming", "duration": "2 Weeks", "learn": ["Classes", "Objects", "Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "Interfaces"]},
                    {"phase": 3, "title": "Desktop UI Development", "duration": "4 Weeks", "learn": ["Windows Forms / WPF", "Controls", "Buttons", "Menus", "Forms", "Dialog Boxes", "Event Handling"]},
                    {"phase": 4, "title": "Advanced UI Design", "duration": "3 Weeks", "learn": ["Layout Panels", "Data Binding", "Themes", "Charts", "Responsive Desktop Design"]},
                    {"phase": 5, "title": "Database Integration", "duration": "3 Weeks", "learn": ["SQLite", "MySQL", "SQL Server", "CRUD Operations", "Stored Procedures"]},
                    {"phase": 6, "title": "File Handling", "duration": "2 Weeks", "learn": ["Read/Write CSV", "Excel Files", "PDF Reports", "JSON", "XML"]},
                    {"phase": 7, "title": "REST API Integration", "duration": "2 Weeks", "learn": ["REST APIs", "HTTP Requests", "JSON Parsing"]},
                    {"phase": 8, "title": "Software Architecture", "duration": "3 Weeks", "learn": ["MVC", "MVVM", "Repository Pattern", "SOLID Principles"]},
                    {"phase": 9, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Merge", "Pull Request"]},
                    {"phase": 10, "title": "Testing & Deployment", "duration": "2 Weeks", "learn": ["Unit Testing", "Debugging", "Logging", "MSI Installer", "ClickOnce Deployment"]},
                    {"phase": 11, "title": "Advanced Desktop Development", "duration": "5 Weeks", "learn": ["Multithreading", "Background Workers", "Printing", "Notifications", "System Tray Applications", "Windows Services"]},
                    {"phase": 12, "title": "Resume & Portfolio", "duration": "1 Week", "learn": ["ATS Resume", "GitHub Portfolio", "LinkedIn Profile", "Desktop Software Portfolio"]},
                    {"phase": 13, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (C#, .NET, WPF, OOP, SQL, Design Patterns, REST APIs)", "HR", "Mock Interviews"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Calculator", "Student Management System", "Library Management System", "To-Do Manager", "Notes Application"],
                    "Intermediate": ["Expense Tracker", "Inventory Management System", "Employee Management System", "Billing Software", "Hotel Management System"],
                    "Advanced": ["Hospital Management System", "Banking Management Software", "College ERP System", "HR Management System", "CRM Desktop Application"],
                    "Industry-Level": ["Enterprise Resource Planning (ERP)", "Accounting Software", "Payroll Management System", "Manufacturing Management System", "Point of Sale (POS) System"]
                },
                "practice_questions": {
                    "Programming": ["250 Coding Problems"],
                    "OOP": ["100 Exercises"],
                    "SQL": ["150 SQL Queries"],
                    "Desktop UI": ["100 UI Challenges"],
                    "REST APIs": ["50 API Integration Exercises"],
                    "File Handling": ["50 Practical Exercises"]
                },
                "certifications": ["C# Programming Certification", ".NET Developer Certification", "WPF Development Certification", "SQL Certification", "Git & GitHub Certification", "Desktop Application Development Certification"],
                "readiness_checklist": ["Programming Fundamentals", "C# / Java / Python", "Object-Oriented Programming", "WinForms / WPF / JavaFX / PyQt", "SQL & Database Design", "SQLite / SQL Server / MySQL", "File Handling (CSV, Excel, PDF)", "REST API Integration", "MVC / MVVM Architecture", "Git & GitHub", "Testing & Debugging", "Application Deployment", "900+ Practice Problems Solved", "15+ Desktop Applications Developed", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Profile Optimized", "15 Mock Interviews Completed", "Ready to Apply for Desktop Application Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 11. Data Analyst
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Data Analyst",
                "slug": "data-analyst",
                "overview": "Career Category: AI & Data Science | Difficulty: Beginner → Intermediate | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹4–8 LPA, Mid-Level (2-5 Yrs): ₹8–15 LPA, Senior: ₹30–50+ LPA",
                "industry_demand": "Very High. Top Recruiters: Google, Microsoft, Amazon, Deloitte, EY, PwC, KPMG, Accenture, Infosys, TCS, Cognizant, Capgemini",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Data Analyst Complete Roadmap",
                "description": "Master data analysis, visualization, and storytelling to drive business decisions. Career Growth: Data Analyst → Senior Data Analyst → Business Analyst → Analytics Manager → Data Scientist.",
                "skills_matrix": {
                    "Core Skills": ["Microsoft Excel", "SQL", "Python", "Statistics", "Data Cleaning", "Data Visualization", "Dashboard Development", "Business Analysis", "Problem Solving"],
                    "Excel": ["Formulas", "Functions", "Pivot Tables", "Power Query", "Charts", "Conditional Formatting", "Data Validation", "Lookup Functions", "Dashboards"],
                    "SQL": ["SELECT", "WHERE", "GROUP BY", "ORDER BY", "JOINs", "Subqueries", "CTE", "Window Functions", "Stored Procedures", "Views"],
                    "Python": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly"],
                    "Statistics": ["Mean", "Median", "Mode", "Standard Deviation", "Probability", "Correlation", "Regression", "Hypothesis Testing"],
                    "Data Visualization": ["Power BI", "Tableau", "Excel Dashboards", "Matplotlib", "Plotly"],
                    "Software & Tools": ["Microsoft Excel", "SQL Server / MySQL", "PostgreSQL", "Power BI", "Tableau", "Python", "Jupyter Notebook", "VS Code", "Git", "GitHub"],
                    "Soft Skills": ["Communication", "Business Understanding", "Critical Thinking", "Storytelling with Data", "Presentation Skills"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Excel Fundamentals", "duration": "4 Weeks", "learn": ["Excel Interface", "Basic Formulas", "Lookup Functions", "Pivot Tables", "Charts", "Dashboards", "Power Query"]},
                    {"phase": 2, "title": "SQL", "duration": "5 Weeks", "learn": ["Database Concepts", "SQL Queries", "Filtering", "Aggregations", "JOINs", "Window Functions", "CTEs", "Views"]},
                    {"phase": 3, "title": "Statistics", "duration": "3 Weeks", "learn": ["Descriptive Statistics", "Inferential Statistics", "Probability", "Hypothesis Testing", "Correlation", "Regression"]},
                    {"phase": 4, "title": "Python", "duration": "5 Weeks", "learn": ["Python Basics", "Functions", "Pandas", "NumPy", "Data Cleaning", "Visualization"]},
                    {"phase": 5, "title": "Power BI", "duration": "4 Weeks", "learn": ["Power Query", "DAX", "Relationships", "Dashboard Design", "KPI Development"]},
                    {"phase": 6, "title": "Tableau", "duration": "2 Weeks", "learn": ["Charts", "Dashboards", "Storytelling", "Filters", "Parameters"]},
                    {"phase": 7, "title": "Business Analytics", "duration": "3 Weeks", "learn": ["KPI Analysis", "Customer Segmentation", "Sales Analysis", "Financial Analysis"]},
                    {"phase": 8, "title": "Git & GitHub", "duration": "1 Week", "learn": ["Repository", "Commit", "Branch", "Push", "Pull Request"]},
                    {"phase": 9, "title": "Portfolio", "duration": "2 Weeks", "learn": ["GitHub Portfolio", "LinkedIn Profile", "ATS Resume", "Power BI Portfolio"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical (Excel, SQL, Python, Statistics, Power BI, Tableau)", "HR", "Business Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Student Result Dashboard", "Sales Dashboard", "HR Dashboard", "Expense Tracker", "Customer Analysis"],
                    "Intermediate": ["Netflix Data Analysis", "IPL Data Analysis", "Hospital Dashboard", "Banking Dashboard", "Retail Sales Dashboard"],
                    "Advanced": ["E-Commerce Analytics", "Supply Chain Dashboard", "Financial Analytics", "Marketing Analytics", "Customer Churn Analysis"],
                    "Industry-Level": ["Blinkit Sales Analysis", "Amazon Sales Dashboard", "Swiggy Business Dashboard", "Zomato Analytics", "Walmart Sales Analytics", "Healthcare Analytics Platform", "Banking Fraud Analysis", "Telecom Customer Analytics"]
                },
                "practice_questions": {
                    "Excel": ["200 Problems"],
                    "SQL": ["500 SQL Queries"],
                    "Python": ["300 Coding Problems"],
                    "Statistics": ["100 Practice Questions"],
                    "Power BI": ["50 Dashboards"],
                    "Tableau": ["30 Dashboards"]
                },
                "certifications": ["Microsoft Excel Certification", "SQL Certification", "Python Certification", "Microsoft Power BI Data Analyst (PL-300)", "Tableau Desktop Specialist", "Google Data Analytics Professional Certificate"],
                "readiness_checklist": ["Excel", "SQL", "Python", "Statistics", "Power BI", "Tableau", "Data Cleaning", "Data Visualization", "Dashboard Development", "Business Analytics", "Git & GitHub", "1,180+ Practice Problems Solved", "20+ Real-World Projects Completed", "Portfolio Website Ready", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for Data Analyst Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 12. Business Analyst
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Business Analyst",
                "slug": "business-analyst",
                "overview": "Career Category: Business & Data Analytics | Difficulty: Beginner → Intermediate | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–9 LPA, Mid-Level: ₹9–18 LPA, Senior: ₹35–60+ LPA",
                "industry_demand": "Very High. Top Recruiters: Deloitte, EY, PwC, KPMG, Accenture, Capgemini, Infosys, TCS, Cognizant, Wipro, Amazon, Microsoft, IBM, Oracle, SAP",
                "who_can_apply": ", ".join(branches) + ", MBA (Business Analytics)"
            },
            {
                "title": "Business Analyst Complete Roadmap",
                "description": "Master business processes, requirements gathering, data analysis, and Agile methodologies. Career Growth: Business Analyst → Senior BA → Lead BA → Business Consultant → Product Owner → Product Manager.",
                "skills_matrix": {
                    "Business Analysis": ["Business Process Analysis", "Requirement Gathering", "Requirement Elicitation", "Requirement Documentation", "Stakeholder Management", "Gap Analysis", "Root Cause Analysis", "SWOT Analysis", "Business Process Modeling", "Business Process Improvement"],
                    "Excel": ["Advanced Formulas", "Pivot Tables", "Power Query", "Dashboards", "Lookup Functions", "Charts", "Data Validation"],
                    "SQL": ["SELECT", "WHERE", "GROUP BY", "HAVING", "JOINs", "Subqueries", "Window Functions", "Views"],
                    "Data Visualization": ["Power BI", "Tableau", "Excel Dashboards"],
                    "Documentation": ["BRD (Business Requirement Document)", "FRD (Functional Requirement Document)", "SRS", "User Stories", "Use Cases", "Process Flows"],
                    "UML & Modeling": ["Flowcharts", "BPMN", "Use Case Diagrams", "Activity Diagrams", "Sequence Diagrams", "ER Diagrams"],
                    "Agile": ["Scrum", "Sprint Planning", "User Stories", "Product Backlog", "Jira", "Confluence"],
                    "Software & Tools": ["Microsoft Excel", "SQL Server / MySQL", "Power BI", "Tableau", "Jira", "Confluence", "Microsoft Visio", "Draw.io", "Lucidchart", "Miro"],
                    "Soft Skills": ["Communication", "Presentation", "Negotiation", "Problem Solving", "Analytical Thinking", "Documentation", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Business Fundamentals", "duration": "3 Weeks", "learn": ["Business Processes", "Organizational Structure", "SDLC", "Business Functions", "Business Terminology"]},
                    {"phase": 2, "title": "Microsoft Excel", "duration": "4 Weeks", "learn": ["Formulas", "Pivot Tables", "Charts", "Dashboards", "Power Query", "Lookup Functions"]},
                    {"phase": 3, "title": "SQL", "duration": "5 Weeks", "learn": ["Database Basics", "SQL Queries", "JOINs", "Window Functions", "CTEs", "Views"]},
                    {"phase": 4, "title": "Requirement Gathering", "duration": "3 Weeks", "learn": ["Requirement Elicitation", "Stakeholder Interviews", "Workshops", "Requirement Prioritization", "Requirement Validation"]},
                    {"phase": 5, "title": "Documentation", "duration": "3 Weeks", "learn": ["BRD", "FRD", "SRS", "User Stories", "Use Cases", "Acceptance Criteria"]},
                    {"phase": 6, "title": "UML & Process Modeling", "duration": "2 Weeks", "learn": ["Flowcharts", "BPMN", "UML", "Process Mapping"]},
                    {"phase": 7, "title": "Power BI & Tableau", "duration": "4 Weeks", "learn": ["Dashboard Development", "KPI Reporting", "Interactive Reports", "Storytelling"]},
                    {"phase": 8, "title": "Agile & Jira", "duration": "2 Weeks", "learn": ["Scrum", "Sprint Planning", "Jira", "Confluence", "Product Backlog"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git Basics", "GitHub", "Documentation Repository", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Business Analysis", "SQL", "Excel", "Agile", "Jira", "Documentation", "UML", "HR", "Business Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Sales Dashboard", "Employee Database Analysis", "Inventory Analysis", "Customer Feedback Analysis", "Expense Tracker"],
                    "Intermediate": ["Hospital Management Requirement Analysis", "Banking Requirement Documentation", "College ERP Business Analysis", "Retail Sales Analytics", "HR Analytics Dashboard"],
                    "Advanced": ["Insurance Claim Management System", "CRM Requirement Analysis", "E-Commerce Business Analysis", "Supply Chain Analytics", "Banking Loan Processing System"],
                    "Industry-Level": ["ERP Business Analysis", "Digital Banking Transformation", "Healthcare Management System", "Retail Business Intelligence Platform", "Airline Reservation System", "Manufacturing ERP Analysis", "Government e-Governance Portal", "Smart City Business Solution"]
                },
                "practice_questions": {
                    "Business Case Studies": ["100 Business Cases"],
                    "Excel": ["200 Problems"],
                    "SQL": ["400 SQL Queries"],
                    "Documentation": ["50 BRDs", "50 FRDs", "50 User Stories"],
                    "UML": ["50 Process Diagrams"],
                    "Dashboard Development": ["30 Power BI Dashboards", "20 Tableau Dashboards"]
                },
                "certifications": ["ECBA (Entry Certificate in Business Analysis)", "CCBA (After Experience)", "CBAP (After Experience)", "Microsoft Excel Certification", "Microsoft Power BI Data Analyst (PL-300)", "Tableau Desktop Specialist", "SQL Certification", "Agile Scrum Certification", "Jira Fundamentals Certification"],
                "readiness_checklist": ["Business Process Analysis", "Requirement Gathering", "BRD & FRD Documentation", "UML & BPMN", "Microsoft Excel", "SQL", "Power BI", "Tableau", "Jira", "Confluence", "Agile Scrum", "Stakeholder Management", "Communication Skills", "950+ Practice Problems Solved", "20+ Real-World Projects Completed", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for Business Analyst Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 13. Business Intelligence (BI) Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Business Intelligence (BI) Developer",
                "slug": "bi-developer",
                "overview": "Career Category: AI & Data Analytics | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–9 LPA, Mid-Level: ₹9–18 LPA, Senior: ₹35–60+ LPA",
                "industry_demand": "Very High. Top Recruiters: Microsoft, Amazon, Google, Deloitte, EY, PwC, KPMG, Accenture, Capgemini, Infosys, TCS, Cognizant, IBM, Oracle, SAP",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Business Intelligence (BI) Developer Complete Roadmap",
                "description": "Master data modeling, ETL, and visualization tools to transform raw data into actionable insights.",
                "skills_matrix": {
                    "Database & SQL": ["Database Fundamentals", "SQL", "Joins", "Window Functions", "CTEs", "Views", "Stored Procedures", "Query Optimization", "Data Modeling"],
                    "Microsoft Excel": ["Advanced Excel", "Pivot Tables", "Power Query", "Power Pivot", "Lookup Functions", "Dynamic Arrays", "Dashboard Design"],
                    "Power BI": ["Power Query", "DAX", "Data Modeling", "Relationships", "Measures", "KPIs", "Dashboard Development", "Report Publishing", "Row-Level Security (RLS)"],
                    "Tableau": ["Dashboard Design", "Storytelling", "Parameters", "Filters", "Calculated Fields", "LOD Expressions"],
                    "ETL & Data Warehousing": ["Data Extraction", "Data Transformation", "Data Loading", "Data Cleaning", "Data Integration", "Star Schema", "Snowflake Schema", "Fact Tables", "Dimension Tables", "OLTP", "OLAP"],
                    "Programming & Cloud": ["Python (Basics)", "Pandas", "NumPy", "Azure Data Services", "AWS Data Analytics", "Google BigQuery"],
                    "Software & Tools": ["Microsoft Excel", "SQL Server", "MySQL", "PostgreSQL", "Power BI Desktop", "Tableau", "SSMS", "Azure Data Studio", "Visual Studio Code", "Python", "Git", "GitHub"],
                    "Soft Skills": ["Business Understanding", "Communication", "Problem Solving", "Data Storytelling", "Presentation Skills"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Excel Fundamentals", "duration": "4 Weeks", "learn": ["Excel Basics", "Formulas", "Lookup Functions", "Pivot Tables", "Power Query", "Dashboard Design"]},
                    {"phase": 2, "title": "SQL", "duration": "5 Weeks", "learn": ["Database Concepts", "SELECT", "WHERE", "GROUP BY", "JOINs", "Window Functions", "CTEs", "Stored Procedures"]},
                    {"phase": 3, "title": "Data Warehousing", "duration": "3 Weeks", "learn": ["Data Warehouse Concepts", "ETL", "Star Schema", "Snowflake Schema", "Fact & Dimension Tables"]},
                    {"phase": 4, "title": "Power BI", "duration": "5 Weeks", "learn": ["Power Query", "DAX", "Relationships", "Measures", "KPIs", "Dashboard Design", "Publishing Reports", "Row-Level Security"]},
                    {"phase": 5, "title": "Tableau", "duration": "3 Weeks", "learn": ["Charts", "Dashboards", "Storytelling", "Parameters", "LOD Expressions"]},
                    {"phase": 6, "title": "Python for BI", "duration": "3 Weeks", "learn": ["Python Basics", "Pandas", "NumPy", "Data Cleaning", "Data Analysis"]},
                    {"phase": 7, "title": "Cloud BI Basics", "duration": "2 Weeks", "learn": ["Azure Data Services", "AWS Analytics", "Google BigQuery", "Cloud Dashboards"]},
                    {"phase": 8, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Portfolio Management", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "Power BI", "Tableau", "Excel", "Data Modeling", "ETL", "DAX", "Python", "HR", "Business Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Sales Dashboard", "Employee Dashboard", "Student Analytics Dashboard", "Expense Dashboard", "Inventory Dashboard"],
                    "Intermediate": ["HR Analytics", "Banking Dashboard", "Healthcare Dashboard", "Retail Analytics", "Financial Reporting Dashboard"],
                    "Advanced": ["E-Commerce BI Solution", "Supply Chain Analytics", "Customer Churn Dashboard", "Marketing Analytics Platform", "Manufacturing BI Dashboard"],
                    "Industry-Level": ["Amazon Sales Analytics", "Walmart Business Intelligence Dashboard", "Hospital BI Platform", "Telecom KPI Dashboard", "Airline Performance Dashboard", "Banking Executive Dashboard", "Government Data Analytics Portal", "Smart City BI Dashboard"]
                },
                "practice_questions": {
                    "Excel": ["200 Problems"],
                    "SQL": ["600 SQL Queries"],
                    "Power BI": ["60 Dashboards"],
                    "Tableau": ["40 Dashboards"],
                    "Python": ["250 Coding Problems"],
                    "Data Modeling": ["50 Data Warehouse Exercises"]
                },
                "certifications": ["Microsoft Power BI Data Analyst (PL-300)", "Tableau Desktop Specialist", "Microsoft Excel Expert", "SQL Certification", "Azure Data Fundamentals (DP-900)", "Azure Data Engineer Associate (DP-203)", "Google Data Analytics Professional Certificate", "Python Certification"],
                "readiness_checklist": ["Microsoft Excel", "Advanced SQL", "Database Design", "Data Warehousing", "ETL Process", "Power BI", "DAX", "Power Query", "Tableau", "Python Basics", "Git & GitHub", "Cloud BI Fundamentals", "Dashboard Design", "KPI Development", "Business Reporting", "1,200+ Practice Problems Solved", "25+ Real-World Dashboards Completed", "Portfolio Website Ready", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for Business Intelligence (BI) Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 14. Data Visualization Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Data Visualization Engineer",
                "slug": "data-visualization-engineer",
                "overview": "Career Category: AI & Data Analytics | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–10 LPA, Mid-Level: ₹10–18 LPA, Senior: ₹35–60+ LPA",
                "industry_demand": "Very High. Top Recruiters: Microsoft, Google, Amazon, Deloitte, EY, PwC, KPMG, Accenture, Infosys, TCS, Cognizant, Capgemini, IBM, Oracle, SAP",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Data Visualization Engineer Complete Roadmap",
                "description": "Master dashboard design, data storytelling, and UI/UX principles to present data effectively using BI tools and web technologies.",
                "skills_matrix": {
                    "Data Visualization": ["Dashboard Design", "Data Storytelling", "KPI Design", "Chart Selection", "Color Theory", "UX/UI Principles", "Interactive Reports", "Report Optimization"],
                    "Microsoft Excel": ["Advanced Formulas", "Pivot Tables", "Power Query", "Charts", "Power Pivot", "Dynamic Dashboards"],
                    "SQL": ["SELECT", "JOINs", "GROUP BY", "HAVING", "CASE", "Window Functions", "CTEs", "Stored Procedures"],
                    "Power BI": ["Power Query", "DAX", "Data Modeling", "Relationships", "Measures", "Row-Level Security", "Dashboard Publishing", "Performance Optimization"],
                    "Tableau": ["Dashboards", "Storytelling", "Parameters", "Filters", "LOD Expressions", "Calculated Fields"],
                    "Python": ["Python Basics", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly"],
                    "Web Visualization (Optional)": ["HTML", "CSS", "JavaScript", "D3.js", "Chart.js"],
                    "Data Modeling": ["Star Schema", "Snowflake Schema", "Fact Tables", "Dimension Tables"],
                    "Software & Tools": ["Microsoft Excel", "SQL Server / MySQL / PostgreSQL", "Power BI Desktop", "Tableau", "Python", "Jupyter Notebook", "VS Code", "Git", "GitHub", "Figma"],
                    "Soft Skills": ["Business Understanding", "Presentation Skills", "Communication", "Problem Solving", "Data Storytelling"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Excel for Visualization", "duration": "4 Weeks", "learn": ["Charts", "Pivot Tables", "Conditional Formatting", "Power Query", "Dashboard Design"]},
                    {"phase": 2, "title": "SQL", "duration": "5 Weeks", "learn": ["Database Concepts", "Advanced SQL", "JOINs", "Window Functions", "Views", "CTEs"]},
                    {"phase": 3, "title": "Visualization Principles", "duration": "2 Weeks", "learn": ["Data Storytelling", "Dashboard Design", "KPI Design", "Visualization Best Practices", "Color Psychology", "User Experience"]},
                    {"phase": 4, "title": "Power BI", "duration": "5 Weeks", "learn": ["Power Query", "DAX", "Data Modeling", "Relationships", "Interactive Reports", "Publishing"]},
                    {"phase": 5, "title": "Tableau", "duration": "3 Weeks", "learn": ["Charts", "Dashboards", "Storytelling", "Parameters", "LOD Expressions"]},
                    {"phase": 6, "title": "Python Visualization", "duration": "4 Weeks", "learn": ["Pandas", "Matplotlib", "Seaborn", "Plotly"]},
                    {"phase": 7, "title": "Web Dashboards", "duration": "2 Weeks", "learn": ["HTML", "CSS", "JavaScript", "Chart.js", "D3.js (Basics)"]},
                    {"phase": 8, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Portfolio Management", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Dashboard Design", "Data Storytelling", "HR", "Business Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Student Dashboard", "Sales Dashboard", "Expense Dashboard", "Employee Dashboard", "Inventory Dashboard"],
                    "Intermediate": ["HR Analytics Dashboard", "Banking Dashboard", "Healthcare Dashboard", "Retail Dashboard", "Customer Analytics Dashboard"],
                    "Advanced": ["E-Commerce Executive Dashboard", "Financial Analytics Platform", "Manufacturing KPI Dashboard", "Supply Chain Dashboard", "Marketing Performance Dashboard"],
                    "Industry-Level": ["Amazon Sales Analytics Dashboard", "Walmart Executive Dashboard", "Hospital Analytics Platform", "Telecom KPI Dashboard", "Airline Operations Dashboard", "Banking Business Intelligence Portal", "Government Analytics Dashboard", "Smart City Visualization Platform"]
                },
                "practice_questions": {
                    "Excel": ["200 Problems"],
                    "SQL": ["600 SQL Queries"],
                    "Power BI": ["60 Dashboards"],
                    "Tableau": ["40 Dashboards"],
                    "Python": ["300 Coding Problems"],
                    "Dashboard Design": ["50 Dashboard UI Challenges"],
                    "Web Visualization": ["30 Interactive Dashboards"]
                },
                "certifications": ["Microsoft Power BI Data Analyst (PL-300)", "Tableau Desktop Specialist", "Microsoft Excel Expert", "SQL Certification", "Python Certification", "Google Data Analytics Professional Certificate", "IBM Data Visualization Certification"],
                "readiness_checklist": ["Advanced Excel", "SQL", "Data Modeling", "Dashboard Design", "Data Storytelling", "Power BI", "DAX", "Tableau", "Python (Pandas, Matplotlib, Plotly)", "Chart.js / D3.js (Basics)", "Git & GitHub", "Business Reporting", "KPI Development", "UX Principles for Dashboards", "1,280+ Practice Problems Solved", "30+ Real-World Dashboards Completed", "Portfolio Website Ready", "GitHub Portfolio Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for Data Visualization Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 15. Database Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Database Developer",
                "slug": "database-developer",
                "overview": "Career Category: Database Engineering / Software Development | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–10 LPA, Mid-Level: ₹10–18 LPA, Senior: ₹35–60+ LPA",
                "industry_demand": "Very High. Top Recruiters: Oracle, Microsoft, IBM, Amazon, Google, SAP, Deloitte, EY, Accenture, Capgemini, Infosys, TCS, Cognizant, Wipro, HCLTech",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Database Developer Complete Roadmap",
                "description": "Master SQL, database design, NoSQL, and query optimization to build robust database solutions. Career Growth: Database Developer → DB Engineer → DBA → Data Engineer → DB Architect.",
                "skills_matrix": {
                    "Database Fundamentals": ["Database Concepts", "Relational Databases (RDBMS)", "DBMS vs RDBMS", "ACID Properties", "Normalization (1NF–BCNF)", "Denormalization", "ER Modeling", "Data Modeling"],
                    "SQL (Core Skill)": ["SELECT", "INSERT", "UPDATE", "DELETE", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "JOINS", "UNION", "Views", "Indexes", "Constraints", "Window Functions", "Common Table Expressions (CTEs)", "Transactions"],
                    "Advanced SQL": ["Stored Procedures", "Functions", "Triggers", "Cursors", "Dynamic SQL", "Query Optimization", "Execution Plans", "Performance Tuning"],
                    "Database Design": ["ER Diagrams", "Schema Design", "Star Schema", "Snowflake Schema", "Data Integrity", "Referential Integrity"],
                    "NoSQL Databases": ["MongoDB", "Firebase Firestore (Basics)", "Redis", "Cassandra (Basics)"],
                    "Programming & ETL": ["Python", "Java", "C#", "SQL Integration", "JDBC / ODBC", "Data Extraction", "Data Transformation", "Data Loading", "Data Validation"],
                    "Cloud Databases": ["Azure SQL Database", "Amazon RDS", "Google Cloud SQL", "PostgreSQL Cloud"],
                    "Software & Tools": ["MySQL", "PostgreSQL", "Microsoft SQL Server", "Oracle Database", "SQLite", "MongoDB", "SSMS", "MySQL Workbench", "pgAdmin", "Oracle SQL Developer", "VS Code", "Git", "GitHub"],
                    "Soft Skills": ["Problem Solving", "Analytical Thinking", "Communication", "Documentation", "Team Collaboration"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Database Fundamentals", "duration": "3 Weeks", "learn": ["DBMS", "RDBMS", "Database Architecture", "ER Diagrams", "Normalization"]},
                    {"phase": 2, "title": "SQL Fundamentals", "duration": "5 Weeks", "learn": ["CRUD Operations", "Filtering", "Sorting", "Aggregate Functions", "JOINS", "Subqueries"]},
                    {"phase": 3, "title": "Advanced SQL", "duration": "4 Weeks", "learn": ["Stored Procedures", "Functions", "Triggers", "Cursors", "Views", "Transactions", "Window Functions"]},
                    {"phase": 4, "title": "Database Design", "duration": "3 Weeks", "learn": ["ER Modeling", "Schema Design", "Constraints", "Indexing", "Query Optimization"]},
                    {"phase": 5, "title": "NoSQL Databases", "duration": "3 Weeks", "learn": ["MongoDB", "Collections", "Documents", "CRUD", "Aggregation Pipeline"]},
                    {"phase": 6, "title": "Programming with Databases", "duration": "4 Weeks", "learn": ["Python Database Connectivity", "JDBC", "ORM Basics", "CRUD Applications"]},
                    {"phase": 7, "title": "Cloud Databases", "duration": "2 Weeks", "learn": ["Azure SQL", "Amazon RDS", "Google Cloud SQL", "Database Backup & Recovery"]},
                    {"phase": 8, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Database Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "Database Design", "Query Optimization", "Transactions", "Indexing", "MongoDB", "Stored Procedures", "HR", "Design Scenarios"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Student Database", "Library Management System", "Employee Database", "Inventory Database", "School Database"],
                    "Intermediate": ["Hospital Database", "Banking Database", "Hotel Management Database", "CRM Database", "Retail Database"],
                    "Advanced": ["E-Commerce Database", "ERP Database", "Airline Reservation Database", "Warehouse Management System", "Supply Chain Database"],
                    "Industry-Level": ["Banking Core Database", "Healthcare Management Database", "Telecom Billing Database", "Manufacturing ERP Database", "University ERP Database", "Government e-Governance Database", "Logistics Management Database", "Financial Data Warehouse"]
                },
                "practice_questions": {
                    "SQL": ["700 SQL Queries"],
                    "Database Design": ["100 ER Diagrams"],
                    "Normalization": ["100 Exercises"],
                    "Stored Procedures & Triggers": ["150 Exercises"],
                    "MongoDB": ["150 Queries"],
                    "Programming": ["250 Coding Problems"]
                },
                "certifications": ["Oracle Database SQL Certified Associate", "Microsoft Azure Database Certification", "MySQL Certification", "PostgreSQL Certification", "MongoDB Associate Developer", "SQL Certification", "Azure Data Fundamentals (DP-900)"],
                "readiness_checklist": ["DBMS & RDBMS Fundamentals", "SQL (Beginner to Advanced)", "Database Design", "ER Modeling", "Normalization", "Stored Procedures", "Triggers", "Views", "Transactions", "Query Optimization", "MongoDB", "Cloud Databases", "Python/Java Database Connectivity", "Git & GitHub", "1,450+ Practice Problems Solved", "25+ Real-World Database Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for Database Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 16. ETL Developer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "ETL Developer",
                "slug": "etl-developer",
                "overview": "Career Category: Data Engineering / Business Intelligence | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹5–9 LPA, Mid-Level: ₹9–18 LPA, Senior: ₹35–60+ LPA",
                "industry_demand": "Very High. Top Recruiters: Accenture, Deloitte, EY, PwC, TCS, Infosys, Cognizant, Capgemini, Wipro, IBM, Oracle, Microsoft, Amazon, Google, HCLTech",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "ETL Developer Complete Roadmap",
                "description": "Master data extraction, transformation, and loading to build robust data pipelines and data warehouses.",
                "skills_matrix": {
                    "Database Fundamentals": ["DBMS", "RDBMS", "ER Modeling", "Data Modeling", "Normalization", "Star Schema", "Snowflake Schema"],
                    "SQL": ["SELECT", "INSERT", "UPDATE", "DELETE", "JOINs", "GROUP BY", "HAVING", "Window Functions", "CTEs", "Views", "Stored Procedures", "Triggers", "Query Optimization"],
                    "ETL Concepts": ["Extract", "Transform", "Load", "Data Cleansing", "Data Validation", "Data Mapping", "Incremental Loading", "Full Loading", "Change Data Capture (CDC)", "Scheduling", "Error Handling", "Logging"],
                    "ETL Tools": ["Informatica PowerCenter", "Talend Open Studio", "Microsoft SSIS", "Pentaho Data Integration (Kettle)", "Apache NiFi", "Azure Data Factory", "AWS Glue", "Oracle Data Integrator (ODI)"],
                    "Data Warehousing": ["Data Warehouse Architecture", "Fact Tables", "Dimension Tables", "Slowly Changing Dimensions (SCD Type 1, 2, 3)", "OLTP", "OLAP"],
                    "Programming & Big Data": ["Python", "Shell Scripting", "Bash", "SQL Scripting", "Hadoop", "Spark", "Hive"],
                    "Cloud Data Services": ["Azure Data Factory", "Azure Synapse Analytics", "AWS Glue", "Amazon Redshift", "Google BigQuery"],
                    "Software & Tools": ["MySQL", "PostgreSQL", "SQL Server", "Oracle Database", "Informatica PowerCenter", "Talend Open Studio", "SSIS", "Pentaho", "Azure Data Factory", "AWS Glue", "VS Code", "Python", "Git", "GitHub"],
                    "Soft Skills": ["Analytical Thinking", "Problem Solving", "Documentation", "Communication", "Time Management"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Database Fundamentals", "duration": "3 Weeks", "learn": ["DBMS", "RDBMS", "ER Modeling", "Normalization", "Data Modeling"]},
                    {"phase": 2, "title": "SQL", "duration": "5 Weeks", "learn": ["CRUD Operations", "JOINs", "Window Functions", "Views", "Stored Procedures", "Query Optimization"]},
                    {"phase": 3, "title": "Data Warehousing", "duration": "3 Weeks", "learn": ["Star Schema", "Snowflake Schema", "Fact & Dimension Tables", "SCD Types", "OLTP vs OLAP"]},
                    {"phase": 4, "title": "ETL Concepts", "duration": "3 Weeks", "learn": ["ETL Process", "Data Mapping", "Data Cleansing", "Data Validation", "Logging", "Scheduling"]},
                    {"phase": 5, "title": "ETL Tools", "duration": "5 Weeks", "learn": ["Informatica PowerCenter", "Talend", "SSIS", "Pentaho"]},
                    {"phase": 6, "title": "Python for ETL", "duration": "3 Weeks", "learn": ["Python Basics", "Pandas", "File Handling", "Database Connectivity", "Automation Scripts"]},
                    {"phase": 7, "title": "Cloud ETL", "duration": "3 Weeks", "learn": ["Azure Data Factory", "AWS Glue", "BigQuery ETL", "Cloud Pipelines"]},
                    {"phase": 8, "title": "Big Data Basics", "duration": "2 Weeks", "learn": ["Hadoop", "Spark", "Hive"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "ETL Concepts", "Informatica", "SSIS", "Talend", "Data Warehouse", "Azure Data Factory", "HR", "Data Migration Scenarios"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["CSV to Database Loader", "Employee Data Migration", "Sales Data Cleaning", "Student Data Import", "Inventory ETL Process"],
                    "Intermediate": ["HR ETL Pipeline", "Banking Data Migration", "Retail Sales ETL", "Hospital Data Integration", "CRM Data Pipeline"],
                    "Advanced": ["Enterprise Data Warehouse ETL", "Financial Data Integration", "Telecom ETL Solution", "Insurance Claims ETL", "Manufacturing Data Pipeline"],
                    "Industry-Level": ["Banking Data Warehouse", "Amazon Sales ETL Pipeline", "Walmart Analytics ETL", "Healthcare Data Integration Platform", "Government Data Migration System", "Telecom Billing ETL", "Airline Reservation ETL", "Smart City Data Pipeline"]
                },
                "practice_questions": {
                    "SQL": ["700 SQL Queries"],
                    "Data Warehouse Design": ["100 Exercises"],
                    "ETL Workflow Development": ["100 ETL Pipelines"],
                    "Informatica / Talend / SSIS": ["50 Real ETL Jobs"],
                    "Python": ["250 Coding Problems"],
                    "Cloud ETL": ["30 Cloud Pipelines"]
                },
                "certifications": ["Informatica PowerCenter Certification", "Microsoft Azure Data Engineer Associate (DP-203)", "Azure Data Fundamentals (DP-900)", "AWS Certified Data Engineer – Associate", "Talend Data Integration Certification", "SQL Certification", "Python Certification"],
                "readiness_checklist": ["Database Fundamentals", "Advanced SQL", "Data Modeling", "Data Warehousing", "ETL Concepts", "Informatica PowerCenter", "Talend / SSIS", "Azure Data Factory", "AWS Glue", "Python", "Git & GitHub", "Cloud ETL", "Big Data Basics", "1,230+ Practice Problems Solved", "25+ Real-World ETL Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "15 Mock Interviews Completed", "Ready to Apply for ETL Developer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 17. Data Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Data Engineer",
                "slug": "data-engineer",
                "overview": "Career Category: Data Engineering / Big Data / Cloud Computing | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹6–12 LPA, Mid-Level: ₹12–22 LPA, Senior: ₹45–80+ LPA",
                "industry_demand": "Very High. Top Recruiters: Google, Microsoft, Amazon, Meta, Netflix, Uber, Oracle, IBM, SAP, Deloitte, EY, Accenture, Infosys, TCS, Cognizant, Capgemini",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Data Engineer Complete Roadmap",
                "description": "Master data infrastructure, big data tools, and cloud platforms to build scalable data pipelines. Career Growth: Data Engineer → Senior Data Engineer → Cloud/Big Data Engineer → Data Architect.",
                "skills_matrix": {
                    "Programming": ["Python", "SQL", "Java (Basics)", "Scala (Optional)"],
                    "SQL": ["CRUD Operations", "Joins", "Subqueries", "CTE", "Window Functions", "Views", "Stored Procedures", "Query Optimization", "Transactions"],
                    "Python": ["Variables", "Loops", "Functions", "OOP", "File Handling", "Exception Handling", "Pandas", "NumPy", "PySpark"],
                    "Database Systems": ["MySQL", "PostgreSQL", "SQL Server", "Oracle", "MongoDB", "Cassandra", "Redis"],
                    "Data Warehousing": ["Star Schema", "Snowflake Schema", "Data Modeling", "Fact Tables", "Dimension Tables", "Slowly Changing Dimensions", "Data Marts"],
                    "ETL & ELT": ["Data Extraction", "Data Transformation", "Data Loading", "Incremental Load", "CDC (Change Data Capture)", "Data Validation", "Data Cleansing"],
                    "ETL Tools": ["Azure Data Factory", "Informatica", "Talend", "SSIS", "AWS Glue", "Apache NiFi"],
                    "Big Data": ["Hadoop", "Spark", "PySpark", "Hive", "Kafka", "HDFS"],
                    "Cloud Platforms": ["Microsoft Azure (Data Factory, Synapse, Blob Storage, Data Lake)", "AWS (S3, Glue, Redshift, EMR, Lambda)", "Google Cloud (BigQuery, Cloud Storage, Dataflow, Dataproc)"],
                    "Workflow Orchestration": ["Apache Airflow", "Prefect (Basics)"],
                    "Linux & Version Control": ["Linux Commands", "Bash Scripting", "Cron Jobs", "Git", "GitHub"],
                    "Soft Skills": ["Problem Solving", "Data Modeling", "Documentation", "Communication", "Team Collaboration"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "SQL Fundamentals", "duration": "5 Weeks", "learn": ["SQL Basics", "CRUD Operations", "JOINs", "GROUP BY", "Window Functions", "Views"]},
                    {"phase": 2, "title": "Python Programming", "duration": "5 Weeks", "learn": ["Python Basics", "OOP", "File Handling", "Pandas", "NumPy"]},
                    {"phase": 3, "title": "Database Systems", "duration": "3 Weeks", "learn": ["MySQL", "PostgreSQL", "MongoDB", "Database Design", "Indexing"]},
                    {"phase": 4, "title": "Data Warehousing", "duration": "3 Weeks", "learn": ["Star Schema", "Snowflake Schema", "Data Modeling", "SCD Types"]},
                    {"phase": 5, "title": "ETL Development", "duration": "4 Weeks", "learn": ["ETL Concepts", "ETL Pipelines", "Data Validation", "ETL Tools"]},
                    {"phase": 6, "title": "Big Data", "duration": "5 Weeks", "learn": ["Hadoop", "Spark", "PySpark", "Hive", "Kafka"]},
                    {"phase": 7, "title": "Cloud Data Engineering", "duration": "4 Weeks", "learn": ["Azure Data Factory", "Azure Synapse", "AWS Glue", "Redshift", "BigQuery"]},
                    {"phase": 8, "title": "Workflow Automation", "duration": "2 Weeks", "learn": ["Apache Airflow", "Scheduling", "DAGs", "Monitoring"]},
                    {"phase": 9, "title": "Git & Docker", "duration": "2 Weeks", "learn": ["Git", "GitHub", "Docker Basics", "Containerization", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Technical Topics (SQL, Python, ETL, Spark, Hadoop, Airflow, Cloud)", "System Design Basics", "HR", "Project Discussion"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Student Database", "Sales Data Pipeline", "CSV to SQL Import Tool", "Employee Database", "Inventory ETL"],
                    "Intermediate": ["Retail Data Warehouse", "Banking ETL Pipeline", "HR Analytics Pipeline", "Customer Data Platform", "Log Processing System"],
                    "Advanced": ["Real-Time Data Pipeline using Kafka", "Azure Data Lake Pipeline", "AWS Glue ETL Solution", "Spark Data Processing Platform", "Streaming Analytics Pipeline"],
                    "Industry-Level": ["E-Commerce Data Lake", "Banking Data Platform", "Healthcare Data Warehouse", "Telecom Analytics Pipeline", "Manufacturing IoT Data Pipeline", "Smart City Data Platform", "Financial Risk Data Platform", "Enterprise Data Engineering Solution"]
                },
                "practice_questions": {
                    "SQL": ["700 SQL Queries"],
                    "Python": ["500 Coding Problems"],
                    "PySpark": ["150 Exercises"],
                    "Data Modeling": ["100 Exercises"],
                    "Spark": ["100 Practical Problems"],
                    "Airflow": ["50 Workflow Exercises"],
                    "Cloud": ["50 Cloud Data Engineering Labs"]
                },
                "certifications": ["Microsoft Azure Data Engineer Associate (DP-203)", "Azure Data Fundamentals (DP-900)", "AWS Certified Data Engineer – Associate", "Google Professional Data Engineer", "Databricks Data Engineer Associate", "Snowflake SnowPro Core Certification", "Apache Spark Certification (Optional)", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["SQL (Advanced)", "Python", "Database Design", "Data Warehousing", "ETL Development", "Apache Spark", "PySpark", "Hadoop", "Kafka", "Apache Airflow", "Azure / AWS / GCP", "Docker", "Git & GitHub", "Linux Basics", "Data Modeling", "Cloud Data Pipelines", "1,650+ Practice Problems Solved", "30+ Real-World Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Data Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 18. Big Data Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Big Data Engineer",
                "slug": "big-data-engineer",
                "overview": "Career Category: Big Data Engineering / Data Engineering / Cloud Computing | Difficulty: Intermediate → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹7–12 LPA, Mid-Level: ₹12–22 LPA, Senior: ₹45–80+ LPA",
                "industry_demand": "Very High. Top Recruiters: Google, Microsoft, Amazon, Meta, Netflix, Uber, Oracle, IBM, SAP, Deloitte, Accenture, Infosys, TCS, Cognizant, Capgemini, Flipkart",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics"
            },
            {
                "title": "Big Data Engineer Complete Roadmap",
                "description": "Master distributed computing, large-scale data processing, and streaming technologies to build enterprise big data platforms.",
                "skills_matrix": {
                    "Programming": ["Python", "SQL", "Java", "Scala (Preferred)"],
                    "SQL": ["CRUD Operations", "JOINs", "Window Functions", "CTEs", "Views", "Stored Procedures", "Query Optimization"],
                    "Big Data Technologies": ["Hadoop", "Apache Spark", "PySpark", "Scala Spark", "Apache Hive", "Apache Kafka", "HDFS", "Apache HBase", "Apache Flume", "Apache Sqoop", "Apache Oozie", "Apache ZooKeeper"],
                    "Distributed Computing": ["Cluster Computing", "Distributed Storage", "Distributed Processing", "Fault Tolerance", "Parallel Processing"],
                    "Data Engineering": ["ETL", "ELT", "Data Pipelines", "Data Warehousing", "Data Lakes", "Data Modeling"],
                    "NoSQL Databases": ["MongoDB", "Cassandra", "HBase", "Redis"],
                    "Cloud Platforms": ["Microsoft Azure (Data Lake, Synapse, Databricks, Event Hub)", "AWS (EMR, S3, Glue, Redshift, Kinesis)", "Google Cloud (BigQuery, Dataproc, Dataflow, Pub/Sub)"],
                    "Workflow & Containerization": ["Apache Airflow", "Apache NiFi", "Docker", "Kubernetes (Basics)"],
                    "Linux & Version Control": ["Linux Commands", "Bash Scripting", "Shell Scripting", "Git", "GitHub"],
                    "Soft Skills": ["Analytical Thinking", "Problem Solving", "Communication", "Documentation", "Team Collaboration"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "SQL & Python", "duration": "5 Weeks", "learn": ["SQL", "Python", "Pandas", "NumPy", "File Handling"]},
                    {"phase": 2, "title": "Database Fundamentals", "duration": "3 Weeks", "learn": ["MySQL", "PostgreSQL", "MongoDB", "Data Modeling", "Database Optimization"]},
                    {"phase": 3, "title": "Hadoop Ecosystem", "duration": "5 Weeks", "learn": ["Hadoop Architecture", "HDFS", "MapReduce", "Hive", "HBase", "Sqoop", "Flume", "Oozie"]},
                    {"phase": 4, "title": "Apache Spark", "duration": "5 Weeks", "learn": ["Spark Core", "Spark SQL", "PySpark", "DataFrames", "RDD", "Spark Streaming"]},
                    {"phase": 5, "title": "Kafka & Streaming", "duration": "3 Weeks", "learn": ["Kafka Producers", "Kafka Consumers", "Topics", "Partitions", "Stream Processing"]},
                    {"phase": 6, "title": "Data Warehousing & ETL", "duration": "3 Weeks", "learn": ["Data Warehouse", "ETL", "ELT", "Star Schema", "Snowflake Schema"]},
                    {"phase": 7, "title": "Cloud Big Data", "duration": "4 Weeks", "learn": ["Azure Databricks", "AWS EMR", "BigQuery", "Redshift", "Azure Data Lake"]},
                    {"phase": 8, "title": "Airflow & Docker", "duration": "2 Weeks", "learn": ["Apache Airflow", "Docker", "Kubernetes Basics"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "Python", "Hadoop", "Spark", "Kafka", "Airflow", "Docker", "Cloud", "HR", "Distributed System Design"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["CSV Processing Tool", "Student Data Pipeline", "Sales Data Analysis", "Log File Processing", "Employee Analytics"],
                    "Intermediate": ["Hadoop Log Analyzer", "Spark Retail Analytics", "Kafka Real-Time Notification System", "ETL Data Pipeline", "Customer Segmentation Platform"],
                    "Advanced": ["Real-Time Fraud Detection Pipeline", "IoT Streaming Analytics", "Social Media Analytics Platform", "Healthcare Big Data Platform", "Cloud-Based Data Lake"],
                    "Industry-Level": ["Netflix Recommendation Data Pipeline", "Amazon Clickstream Analytics", "Banking Fraud Detection Platform", "Smart City Data Platform", "Telecom Real-Time Analytics", "Manufacturing IoT Analytics", "E-Commerce Data Lake", "Enterprise Big Data Platform"]
                },
                "practice_questions": {
                    "SQL": ["700 SQL Queries"],
                    "Python": ["500 Coding Problems"],
                    "Hadoop": ["150 Practical Labs"],
                    "Spark / PySpark": ["200 Exercises"],
                    "Kafka": ["100 Streaming Exercises"],
                    "Airflow": ["50 Workflow Projects"],
                    "Docker": ["50 Containerization Exercises"],
                    "Cloud": ["50 Big Data Labs"]
                },
                "certifications": ["Databricks Data Engineer Associate", "Microsoft Azure Data Engineer Associate (DP-203)", "Google Professional Data Engineer", "AWS Certified Data Engineer – Associate", "Cloudera Data Platform Certification", "Apache Spark Certification", "Snowflake SnowPro Core", "SQL Certification", "Python Certification"],
                "readiness_checklist": ["Advanced SQL", "Python", "Hadoop Ecosystem", "Apache Spark", "PySpark", "Apache Kafka", "Hive", "HDFS", "Data Warehousing", "ETL Development", "Apache Airflow", "Docker", "Azure / AWS / GCP", "Git & GitHub", "Linux Basics", "1,750+ Practice Problems Solved", "30+ Real-World Big Data Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Big Data Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 19. Analytics Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Analytics Engineer",
                "slug": "analytics-engineer",
                "overview": "Career Category: Analytics Engineering / Data Engineering / Business Intelligence | Difficulty: Beginner → Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹6–12 LPA, Mid-Level: ₹12–22 LPA, Senior: ₹40–70+ LPA",
                "industry_demand": "Very High. Top Recruiters: Google, Microsoft, Amazon, Meta, Netflix, Uber, Airbnb, Deloitte, EY, PwC, Accenture, TCS, Infosys, Cognizant, Capgemini, Flipkart",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Statistics, Biotechnology Engineering"
            },
            {
                "title": "Analytics Engineer Complete Roadmap",
                "description": "Bridge the gap between data engineering and data analysis by building scalable data models, transforming data, and implementing BI solutions.",
                "skills_matrix": {
                    "SQL": ["SELECT", "INSERT", "UPDATE", "DELETE", "JOINs", "GROUP BY", "HAVING", "Window Functions", "CTEs", "Views", "Stored Procedures", "Query Optimization"],
                    "Python": ["Python Basics", "Pandas", "NumPy", "File Handling", "Data Cleaning", "Data Transformation", "APIs"],
                    "Excel": ["Advanced Formulas", "Pivot Tables", "Power Query", "Power Pivot", "Dashboards", "Data Validation"],
                    "Business Intelligence": ["Power BI", "Tableau", "Looker", "Looker Studio", "Qlik Sense (Basics)"],
                    "Data Modeling": ["Star Schema", "Snowflake Schema", "Fact Tables", "Dimension Tables", "Slowly Changing Dimensions", "ER Modeling"],
                    "Analytics Engineering": ["dbt (Data Build Tool)", "Data Transformation", "Semantic Layer", "Data Testing", "Documentation", "Data Lineage"],
                    "Data Warehousing": ["Snowflake", "Google BigQuery", "Amazon Redshift", "Azure Synapse", "PostgreSQL"],
                    "ETL / ELT": ["Data Pipelines", "Incremental Loading", "Data Cleansing", "Data Validation", "Workflow Automation"],
                    "Cloud Platforms": ["Azure (Synapse, Data Factory)", "AWS (Redshift, Glue)", "Google Cloud (BigQuery, Cloud Storage)"],
                    "Software & Tools": ["VS Code", "Jupyter Notebook", "MySQL", "PostgreSQL", "Snowflake", "BigQuery", "dbt", "Power BI", "Tableau", "Looker", "Excel", "Git", "GitHub"],
                    "Soft Skills": ["Business Communication", "Data Storytelling", "Problem Solving", "Critical Thinking", "Documentation"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "SQL", "duration": "5 Weeks", "learn": ["SQL Basics", "Advanced SQL", "Window Functions", "Query Optimization"]},
                    {"phase": 2, "title": "Python", "duration": "4 Weeks", "learn": ["Python", "Pandas", "NumPy", "Data Cleaning", "Data Transformation"]},
                    {"phase": 3, "title": "Excel", "duration": "2 Weeks", "learn": ["Advanced Excel", "Power Query", "Power Pivot", "Dashboards"]},
                    {"phase": 4, "title": "Data Modeling", "duration": "3 Weeks", "learn": ["Star Schema", "Snowflake Schema", "Fact & Dimension Tables", "Data Warehouse Design"]},
                    {"phase": 5, "title": "dbt & Analytics Engineering", "duration": "4 Weeks", "learn": ["dbt Models", "Data Testing", "Data Documentation", "Data Lineage", "Semantic Layer"]},
                    {"phase": 6, "title": "Business Intelligence", "duration": "4 Weeks", "learn": ["Power BI", "Tableau", "Looker", "Dashboard Design", "KPI Development"]},
                    {"phase": 7, "title": "Cloud Data Warehousing", "duration": "3 Weeks", "learn": ["Snowflake", "BigQuery", "Redshift", "Azure Synapse"]},
                    {"phase": 8, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["SQL", "dbt", "Data Modeling", "BI Tools", "Cloud Warehouses", "Dashboard Design", "HR", "Business Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Sales Dashboard", "Student Analytics", "Customer Analysis", "Employee Analytics", "Inventory Dashboard"],
                    "Intermediate": ["Retail Analytics Platform", "HR Analytics Dashboard", "Banking Analytics", "Hospital Analytics", "Marketing Performance Dashboard"],
                    "Advanced": ["End-to-End Analytics Engineering Pipeline", "Cloud Data Warehouse", "Customer 360 Analytics", "Enterprise KPI Dashboard", "Revenue Analytics Platform"],
                    "Industry-Level": ["Amazon Business Analytics Platform", "Netflix User Analytics", "Banking Executive Dashboard", "Telecom Customer Analytics", "Manufacturing Performance Analytics", "E-Commerce Analytics Pipeline", "Healthcare Analytics Platform", "Smart City Analytics Dashboard"]
                },
                "practice_questions": {
                    "SQL": ["800 SQL Queries"],
                    "Python": ["350 Coding Problems"],
                    "Excel": ["200 Dashboard Exercises"],
                    "dbt": ["100 Data Transformation Models"],
                    "Power BI": ["50 Dashboards"],
                    "Tableau": ["30 Dashboards"],
                    "Looker": ["20 Analytics Projects"],
                    "Data Modeling": ["100 Exercises"]
                },
                "certifications": ["dbt Fundamentals Certification", "Microsoft Power BI Data Analyst (PL-300)", "Tableau Desktop Specialist", "Google Data Analytics Professional Certificate", "Snowflake SnowPro Core Certification", "Google Professional Data Engineer", "Azure Data Engineer Associate (DP-203)", "SQL Certification", "Python Certification"],
                "readiness_checklist": ["Advanced SQL", "Python", "Advanced Excel", "Data Modeling", "dbt", "Data Warehousing", "Snowflake / BigQuery", "Power BI", "Tableau", "Looker", "Git & GitHub", "Cloud Platforms", "Data Storytelling", "Business KPI Design", "1,650+ Practice Problems Solved", "35+ Real-World Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Analytics Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 20. NLP (Natural Language Processing) Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "NLP (Natural Language Processing) Engineer",
                "slug": "nlp-engineer",
                "overview": "Career Category: Artificial Intelligence / Machine Learning / Generative AI | Difficulty: Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹8–15 LPA, Mid-Level: ₹15–30 LPA, Senior: ₹60 LPA–₹1 Cr+",
                "industry_demand": "Very High. Top Recruiters: OpenAI, Google, Microsoft, Amazon, Apple, Meta, NVIDIA, Adobe, IBM, Oracle, Salesforce, Deloitte, Accenture, TCS, Infosys, Qualcomm",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Computing, Statistics, Data Science, Computational Linguistics"
            },
            {
                "title": "NLP (Natural Language Processing) Engineer Complete Roadmap",
                "description": "Master natural language processing, deep learning, and large language models to build intelligent text and speech applications.",
                "skills_matrix": {
                    "Programming & Math": ["Python", "SQL", "Java (Basics)", "C++ (Optional)", "Linear Algebra", "Probability", "Statistics", "Calculus", "Optimization"],
                    "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Feature Engineering", "Cross Validation", "Hyperparameter Tuning", "NumPy", "Pandas", "Scikit-learn"],
                    "Deep Learning": ["Neural Networks", "CNN", "RNN", "LSTM", "GRU", "Attention Mechanism", "Transformers"],
                    "NLP Core": ["Tokenization", "Lemmatization", "Stemming", "TF-IDF", "Word Embeddings", "Word2Vec", "GloVe", "NER", "POS Tagging", "Sentiment Analysis", "Text Classification", "Topic Modeling", "Machine Translation"],
                    "Large Language Models (LLMs)": ["GPT Models", "Llama", "Mistral", "Gemini", "Claude", "Prompt Engineering", "Fine Tuning", "RAG", "AI Agents", "Function Calling"],
                    "NLP Frameworks": ["NLTK", "spaCy", "Hugging Face Transformers", "TensorFlow", "PyTorch", "LangChain", "LlamaIndex", "Sentence Transformers"],
                    "Databases & Vector DBs": ["SQL", "MongoDB", "PostgreSQL", "FAISS", "ChromaDB", "Pinecone", "Weaviate", "Milvus"],
                    "Cloud & Deployment": ["Azure AI", "AWS SageMaker", "Vertex AI", "FastAPI", "Flask", "Docker", "Kubernetes", "REST APIs"],
                    "Software & Tools": ["Python", "VS Code", "Jupyter Notebook", "Google Colab", "Git", "GitHub", "Docker", "Hugging Face", "LangChain", "Ollama"],
                    "Soft Skills": ["Problem Solving", "Research Skills", "Communication", "Documentation", "Critical Thinking"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Python & SQL", "duration": "4 Weeks", "learn": ["Python", "OOP", "SQL", "Pandas", "NumPy"]},
                    {"phase": 2, "title": "Mathematics & Machine Learning", "duration": "4 Weeks", "learn": ["Statistics", "Linear Algebra", "Machine Learning", "Feature Engineering"]},
                    {"phase": 3, "title": "Deep Learning", "duration": "4 Weeks", "learn": ["Neural Networks", "CNN", "RNN", "LSTM", "Transformers"]},
                    {"phase": 4, "title": "NLP Fundamentals", "duration": "5 Weeks", "learn": ["Tokenization", "Lemmatization", "TF-IDF", "Word Embeddings", "NER", "POS Tagging", "Sentiment Analysis"]},
                    {"phase": 5, "title": "Advanced NLP", "duration": "4 Weeks", "learn": ["Hugging Face", "BERT", "RoBERTa", "GPT", "T5", "Text Summarization", "Machine Translation"]},
                    {"phase": 6, "title": "Generative AI & LLMs", "duration": "4 Weeks", "learn": ["Prompt Engineering", "LangChain", "RAG", "LlamaIndex", "AI Agents", "Fine-Tuning", "Vector Databases"]},
                    {"phase": 7, "title": "Deployment", "duration": "2 Weeks", "learn": ["FastAPI", "Flask", "Docker", "REST APIs"]},
                    {"phase": 8, "title": "Cloud AI", "duration": "2 Weeks", "learn": ["Azure AI", "AWS Bedrock", "Vertex AI"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Python", "NLP", "Deep Learning", "Transformers", "LLMs", "RAG", "LangChain", "HR", "AI Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Spam Email Classifier", "Sentiment Analysis", "Resume Parser", "Language Translator", "Text Summarizer"],
                    "Intermediate": ["AI Chatbot", "Fake News Detector", "Question Answering System", "Named Entity Recognition", "Text Classification Platform"],
                    "Advanced": ["GPT-Powered AI Assistant", "Enterprise Document Search (RAG)", "AI Customer Support Chatbot", "AI Resume Screening System", "Medical NLP Assistant"],
                    "Industry-Level": ["Legal Document Intelligence Platform", "Healthcare Clinical NLP System", "Financial AI Assistant", "AI Research Paper Summarizer", "Multi-Language Translation Platform", "Voice-to-Text AI Platform", "Enterprise Knowledge Chatbot", "AI Customer Service Platform"]
                },
                "practice_questions": {
                    "Python": ["600 Coding Problems"],
                    "SQL": ["500 SQL Queries"],
                    "Machine Learning": ["150 ML Problems"],
                    "Deep Learning": ["150 Practical Labs"],
                    "NLP": ["250 NLP Exercises"],
                    "Transformers": ["100 Projects"],
                    "LangChain & RAG": ["50 AI Applications"],
                    "LLM Fine-Tuning": ["30 Projects"]
                },
                "certifications": ["Hugging Face NLP Course", "DeepLearning.AI Generative AI", "Google Professional Machine Learning Engineer", "Microsoft Azure AI Engineer Associate (AI-102)", "AWS Certified Machine Learning Engineer", "TensorFlow Developer Certificate", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["Advanced Python", "Advanced SQL", "Mathematics", "Machine Learning", "Deep Learning", "NLP Fundamentals", "Transformers", "Hugging Face", "LangChain", "RAG", "Vector Databases", "LLM Fine-Tuning", "FastAPI", "Docker", "Git & GitHub", "Cloud AI (Azure/AWS/GCP)", "1,830+ Practice Problems Solved", "35+ Real-World AI & NLP Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for NLP (Natural Language Processing) Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 21. Computer Vision Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Computer Vision Engineer",
                "slug": "computer-vision-engineer",
                "overview": "Career Category: Artificial Intelligence / Deep Learning / Computer Vision | Difficulty: Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹8–15 LPA, Mid-Level: ₹15–30 LPA, Senior: ₹60 LPA–₹1 Cr+",
                "industry_demand": "Very High. Top Recruiters: Google, Microsoft, Amazon, Apple, NVIDIA, Tesla, Qualcomm, Intel, Samsung, Bosch, Continental, Siemens, Meta, OpenAI, Adobe",
                "who_can_apply": ", ".join(branches) + ", Robotics Engineering, Mechatronics Engineering, Biomedical Engineering, Mathematics & Computing"
            },
            {
                "title": "Computer Vision Engineer Complete Roadmap",
                "description": "Master image processing, object detection, and deep learning architectures to build advanced vision systems.",
                "skills_matrix": {
                    "Programming & Math": ["Python", "SQL", "C++", "Java (Basics)", "Linear Algebra", "Probability", "Statistics", "Calculus", "Optimization"],
                    "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Model Evaluation", "Cross Validation", "NumPy", "Pandas", "Scikit-image"],
                    "Computer Vision Basics": ["OpenCV", "Digital Image Processing", "Image Enhancement", "Feature Extraction", "Edge Detection", "Histogram Equalization", "Morphological Operations"],
                    "Deep Learning": ["Neural Networks", "CNN", "Transfer Learning", "Autoencoders", "GANs", "Vision Transformers (ViT)"],
                    "CV Applications": ["Face Detection", "Face Recognition", "Image Classification", "Object Detection", "Object Tracking", "Image Segmentation", "OCR", "Pose Estimation", "Action Recognition", "Video Analytics"],
                    "Frameworks & AI": ["TensorFlow", "Keras", "PyTorch", "OpenCV DNN", "ONNX", "Hugging Face", "YOLO", "Detectron2", "MMDetection", "MediaPipe"],
                    "Cloud AI": ["Azure AI Vision", "Azure Machine Learning", "AWS Rekognition", "SageMaker", "Vertex AI", "Vision AI API"],
                    "Deployment & Tools": ["FastAPI", "Flask", "Docker", "Kubernetes", "REST APIs", "Git", "GitHub"],
                    "Soft Skills": ["Problem Solving", "Research Skills", "Documentation", "Communication", "Analytical Thinking"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Python & SQL", "duration": "4 Weeks", "learn": ["Python", "SQL", "Pandas", "NumPy", "File Handling"]},
                    {"phase": 2, "title": "Mathematics & Machine Learning", "duration": "4 Weeks", "learn": ["Linear Algebra", "Statistics", "Machine Learning", "Feature Engineering"]},
                    {"phase": 3, "title": "OpenCV & Image Processing", "duration": "5 Weeks", "learn": ["OpenCV", "Image Processing", "Edge Detection", "Filtering", "Histograms", "Feature Detection"]},
                    {"phase": 4, "title": "Deep Learning", "duration": "5 Weeks", "learn": ["CNN", "Transfer Learning", "TensorFlow", "PyTorch", "Keras"]},
                    {"phase": 5, "title": "Advanced Computer Vision", "duration": "5 Weeks", "learn": ["YOLO", "Object Detection", "Image Segmentation", "OCR", "Pose Estimation", "Video Processing"]},
                    {"phase": 6, "title": "Vision AI & Generative AI", "duration": "4 Weeks", "learn": ["Vision Transformers (ViT)", "CLIP", "SAM (Segment Anything)", "Diffusion Models", "Multimodal AI"]},
                    {"phase": 7, "title": "Deployment", "duration": "2 Weeks", "learn": ["FastAPI", "Flask", "Docker", "REST APIs"]},
                    {"phase": 8, "title": "Cloud AI", "duration": "2 Weeks", "learn": ["Azure AI Vision", "AWS Rekognition", "Google Vision AI"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Python", "OpenCV", "CNN", "YOLO", "PyTorch", "TensorFlow", "Object Detection", "HR", "Vision AI Case Studies"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["Face Detection System", "Image Filter App", "Image Classifier", "OCR Scanner", "QR Code Scanner"],
                    "Intermediate": ["Vehicle Detection System", "Face Recognition Attendance System", "License Plate Recognition", "Hand Gesture Recognition", "Medical Image Classification"],
                    "Advanced": ["Autonomous Driving Vision System", "AI Surveillance System", "Smart Retail Object Detection", "Real-Time Video Analytics", "AI Drone Vision System"],
                    "Industry-Level": ["Self-Driving Car Vision Pipeline", "Smart City CCTV Analytics", "AI-Based Medical Imaging Diagnosis", "Manufacturing Quality Inspection System", "Retail Shelf Monitoring Platform", "Face Recognition Security Platform", "AI Sports Analytics Platform", "Industrial Defect Detection System"]
                },
                "practice_questions": {
                    "Python": ["600 Coding Problems"],
                    "SQL": ["500 SQL Queries"],
                    "OpenCV": ["250 Practical Exercises"],
                    "Machine Learning": ["150 ML Problems"],
                    "Deep Learning": ["200 Deep Learning Labs"],
                    "YOLO": ["100 Object Detection Projects"],
                    "Image Processing": ["150 Image Processing Exercises"],
                    "Vision AI": ["50 Advanced AI Projects"]
                },
                "certifications": ["OpenCV Certification", "TensorFlow Developer Certificate", "PyTorch Certification", "NVIDIA Deep Learning Institute Certification", "Microsoft Azure AI Engineer Associate (AI-102)", "Google Professional Machine Learning Engineer", "AWS Machine Learning Engineer", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["Advanced Python", "Advanced SQL", "Mathematics", "Machine Learning", "Deep Learning", "OpenCV", "TensorFlow", "PyTorch", "CNN", "YOLO", "Vision Transformers", "Image Processing", "Object Detection", "OCR", "FastAPI", "Docker", "Git & GitHub", "Cloud Vision AI", "2,000+ Practice Problems Solved", "35+ Real-World Computer Vision Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Computer Vision Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 22. Generative AI Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Generative AI Engineer",
                "slug": "generative-ai-engineer",
                "overview": "Career Category: Artificial Intelligence / Generative AI / Large Language Models (LLMs) | Difficulty: Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹10–18 LPA, Mid-Level: ₹18–35 LPA, Senior: ₹70 LPA–₹1.5 Cr+",
                "industry_demand": "Extremely High. Top Recruiters: OpenAI, Google DeepMind, Anthropic, Microsoft, Meta, Amazon, NVIDIA, Apple, Adobe, Salesforce, Oracle, IBM, Deloitte, EY, Accenture, TCS, Infosys, Cognizant, Capgemini",
                "who_can_apply": ", ".join(branches) + ", Robotics Engineering, Mathematics & Computing, Data Science, Statistics"
            },
            {
                "title": "Generative AI Engineer Complete Roadmap",
                "description": "Master large language models, prompt engineering, RAG, and AI agents to build next-generation AI applications.",
                "skills_matrix": {
                    "Programming & Math": ["Python", "SQL", "JavaScript (Basics)", "C++ (Optional)", "Linear Algebra", "Probability", "Statistics", "Calculus", "Optimization"],
                    "Machine & Deep Learning": ["Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Neural Networks", "CNN", "RNN", "Transformers", "Attention Mechanism", "Autoencoders", "GANs", "Diffusion Models"],
                    "Generative AI Core": ["LLMs", "Prompt Engineering", "RAG", "AI Agents", "Function Calling", "Fine-Tuning", "PEFT (LoRA, QLoRA)", "RLHF", "Multimodal AI", "AI Evaluation", "Hallucination Mitigation"],
                    "LLM Frameworks": ["Hugging Face Transformers", "LangChain", "LangGraph", "LlamaIndex", "Haystack", "CrewAI", "AutoGen", "Semantic Kernel"],
                    "Models & APIs": ["OpenAI API", "GPT Models", "Embeddings", "Llama", "Mistral", "Gemma", "Qwen", "DeepSeek", "Falcon"],
                    "Databases & Vector DBs": ["Pinecone", "ChromaDB", "FAISS", "Weaviate", "Milvus", "Qdrant", "PostgreSQL", "MySQL", "MongoDB", "Redis"],
                    "Backend & Deployment": ["FastAPI", "Flask", "GraphQL (Basics)", "Docker", "Kubernetes", "CI/CD", "Nginx"],
                    "Cloud AI & MLOps": ["Azure AI Foundry", "Amazon Bedrock", "Vertex AI", "Gemini API", "MLflow", "Weights & Biases", "DVC", "Model Monitoring"],
                    "Soft Skills": ["Problem Solving", "Research", "Communication", "AI Ethics", "Technical Documentation"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Python & SQL", "duration": "4 Weeks", "learn": ["Python", "SQL", "OOP", "Pandas", "NumPy"]},
                    {"phase": 2, "title": "Mathematics & Machine Learning", "duration": "4 Weeks", "learn": ["Linear Algebra", "Statistics", "Machine Learning", "Model Evaluation"]},
                    {"phase": 3, "title": "Deep Learning", "duration": "4 Weeks", "learn": ["Neural Networks", "CNN", "RNN", "Transformers", "Attention"]},
                    {"phase": 4, "title": "LLM Fundamentals", "duration": "5 Weeks", "learn": ["GPT Models", "Prompt Engineering", "Tokenization", "Embeddings", "Context Windows", "Function Calling"]},
                    {"phase": 5, "title": "Advanced Generative AI", "duration": "5 Weeks", "learn": ["LangChain", "LangGraph", "LlamaIndex", "AI Agents", "Multi-Agent Systems", "Workflow Automation"]},
                    {"phase": 6, "title": "RAG & Vector Databases", "duration": "4 Weeks", "learn": ["RAG Architecture", "Pinecone", "ChromaDB", "FAISS", "AI Search"]},
                    {"phase": 7, "title": "Fine-Tuning & Multimodal AI", "duration": "3 Weeks", "learn": ["LoRA", "QLoRA", "PEFT", "Diffusion Models", "Image Generation", "Multimodal AI"]},
                    {"phase": 8, "title": "Deployment & Cloud", "duration": "3 Weeks", "learn": ["FastAPI", "Docker", "Azure OpenAI", "Amazon Bedrock", "Vertex AI"]},
                    {"phase": 9, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 10, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Python", "LLMs", "RAG", "Prompt Engineering", "AI Agents", "Vector Databases", "FastAPI", "HR", "System Design"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["AI Text Summarizer", "Resume Analyzer", "AI Translator", "FAQ Chatbot", "AI Email Generator"],
                    "Intermediate": ["PDF Chat Assistant", "AI Customer Support Bot", "AI Code Generator", "AI Research Assistant", "AI Content Generator"],
                    "Advanced": ["Enterprise RAG Chatbot", "Multi-Agent AI System", "AI Copilot for Developers", "AI Legal Assistant", "AI Healthcare Assistant"],
                    "Industry-Level": ["Enterprise Knowledge Management Platform", "AI Financial Advisor", "AI HR Recruitment Assistant", "AI Education Tutor", "AI Software Development Assistant", "AI Medical Diagnosis Assistant", "AI Contract Review System", "AI Customer Success Platform"]
                },
                "practice_questions": {
                    "Python": ["700 Coding Problems"],
                    "SQL": ["500 SQL Queries"],
                    "Machine Learning": ["200 ML Problems"],
                    "Deep Learning": ["200 Practical Labs"],
                    "Prompt Engineering": ["150 Prompt Challenges"],
                    "RAG Applications": ["100 Projects"],
                    "AI Agents": ["80 Agent Workflows"],
                    "Vector Databases": ["70 Practical Exercises"],
                    "LLM Fine-Tuning": ["50 Labs"]
                },
                "certifications": ["Microsoft Azure AI Engineer Associate (AI-102)", "Google Professional Machine Learning Engineer", "AWS Certified Machine Learning Engineer", "DeepLearning.AI Generative AI Specialization", "Hugging Face AI Course", "NVIDIA Generative AI Certification", "LangChain Academy", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["Advanced Python", "Advanced SQL", "Machine Learning", "Deep Learning", "Transformers", "Prompt Engineering", "LLM Development", "LangChain", "LangGraph", "LlamaIndex", "AI Agents", "RAG", "Vector Databases", "FastAPI", "Docker", "Azure AI / AWS Bedrock / Vertex AI", "Git & GitHub", "2,050+ Practice Problems Solved", "40+ Real-World Generative AI Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Generative AI Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 23. LLM (Large Language Model) Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "LLM (Large Language Model) Engineer",
                "slug": "llm-engineer",
                "overview": "Career Category: Artificial Intelligence / Large Language Models / Generative AI | Difficulty: Advanced | Learning Duration: 6–12 Months.",
                "india_salary": "Fresher: ₹10–18 LPA, Mid-Level: ₹18–35 LPA, Senior: ₹70 LPA–₹1.5 Cr+",
                "industry_demand": "Extremely High. Top Recruiters: OpenAI, Google DeepMind, Anthropic, Microsoft, Meta, Amazon, NVIDIA, Apple, Oracle, IBM, Adobe, Salesforce, Cohere, Mistral AI, Hugging Face",
                "who_can_apply": ", ".join(branches) + ", Mathematics & Computing, Robotics Engineering, Data Science, Statistics, Computational Linguistics"
            },
            {
                "title": "LLM (Large Language Model) Engineer Complete Roadmap",
                "description": "Specialize in large language models, fine-tuning, retrieval-augmented generation (RAG), and building sophisticated AI agents.",
                "skills_matrix": {
                    "Programming & Math": ["Python", "SQL", "JavaScript (Basics)", "C++ (Optional)", "Linear Algebra", "Probability", "Statistics", "Calculus", "Optimization"],
                    "Machine & Deep Learning": ["Supervised Learning", "Unsupervised Learning", "Neural Networks", "CNN", "RNN", "LSTM", "Transformers", "Attention Mechanism"],
                    "NLP Fundamentals": ["Tokenization", "TF-IDF", "Word2Vec", "FastText", "GloVe", "BERT", "RoBERTa", "T5"],
                    "LLM Core": ["LLM Architecture", "Prompt Engineering", "Context Windows", "Embeddings", "Function Calling", "RAG", "AI Agents", "Fine-Tuning", "PEFT", "RLHF", "Quantization"],
                    "LLM Frameworks": ["Hugging Face Transformers", "LangChain", "LangGraph", "LlamaIndex", "Haystack", "Semantic Kernel", "CrewAI", "AutoGen"],
                    "Models & Vector DBs": ["GPT Models", "Llama", "Mistral", "Gemma", "DeepSeek", "Pinecone", "ChromaDB", "FAISS", "Weaviate", "Milvus", "Qdrant"],
                    "Backend & Deployment": ["FastAPI", "Flask", "Docker", "Kubernetes", "CI/CD", "PostgreSQL", "MySQL", "MongoDB", "Redis"],
                    "Cloud AI & MLOps": ["Azure AI Foundry", "Amazon Bedrock", "Vertex AI", "MLflow", "Weights & Biases", "DVC", "Model Monitoring"],
                    "Soft Skills": ["Research", "Problem Solving", "Communication", "Technical Documentation", "AI Ethics"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Python & SQL", "duration": "4 Weeks", "learn": ["Python", "SQL", "OOP", "Pandas", "NumPy"]},
                    {"phase": 2, "title": "Mathematics & Machine Learning", "duration": "4 Weeks", "learn": ["Linear Algebra", "Probability", "Statistics", "Machine Learning"]},
                    {"phase": 3, "title": "Deep Learning & NLP", "duration": "5 Weeks", "learn": ["Neural Networks", "Transformers", "BERT", "GPT", "NLP Fundamentals"]},
                    {"phase": 4, "title": "LLM Development", "duration": "5 Weeks", "learn": ["GPT", "Llama", "Mistral", "Prompt Engineering", "Embeddings", "Context Management"]},
                    {"phase": 5, "title": "RAG & AI Agents", "duration": "5 Weeks", "learn": ["LangChain", "LangGraph", "LlamaIndex", "RAG", "AI Agents", "Multi-Agent Systems"]},
                    {"phase": 6, "title": "Fine-Tuning & Optimization", "duration": "4 Weeks", "learn": ["LoRA", "QLoRA", "PEFT", "Quantization", "Model Evaluation", "Inference Optimization"]},
                    {"phase": 7, "title": "Deployment & Cloud", "duration": "3 Weeks", "learn": ["FastAPI", "Docker", "Azure OpenAI", "Amazon Bedrock", "Vertex AI"]},
                    {"phase": 8, "title": "Git & Portfolio", "duration": "1 Week", "learn": ["Git", "GitHub", "Documentation", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "3 Weeks", "learn": ["Python", "Transformers", "LLMs", "RAG", "AI Agents", "Vector Databases", "System Design", "HR"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "6 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "8 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "10 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["AI Text Summarizer", "Resume Analyzer", "FAQ Chatbot", "AI Translator", "Smart Email Generator"],
                    "Intermediate": ["PDF Chatbot", "AI Coding Assistant", "AI Research Assistant", "Customer Support Chatbot", "AI Document Search"],
                    "Advanced": ["Enterprise RAG Platform", "AI Multi-Agent System", "AI Software Development Copilot", "AI Legal Assistant", "AI Healthcare Assistant"],
                    "Industry-Level": ["Enterprise Knowledge Management Platform", "AI Financial Advisor", "AI HR Recruitment Platform", "AI Learning Assistant", "AI Customer Support Suite", "AI Medical Diagnosis Assistant", "AI Contract Intelligence System", "AI Enterprise Search Engine"]
                },
                "practice_questions": {
                    "Python": ["700 Coding Problems"],
                    "SQL": ["500 SQL Queries"],
                    "Machine Learning": ["200 ML Problems"],
                    "Deep Learning": ["200 Practical Labs"],
                    "NLP": ["250 NLP Exercises"],
                    "Prompt Engineering": ["200 Prompt Challenges"],
                    "LLM Development": ["120 Practical Projects"],
                    "AI Agents": ["80 Workflows"],
                    "RAG": ["100 Projects"],
                    "Fine-Tuning": ["50 Labs"]
                },
                "certifications": ["Microsoft Azure AI Engineer Associate (AI-102)", "Google Professional Machine Learning Engineer", "AWS Certified Machine Learning Engineer", "Hugging Face AI Course", "DeepLearning.AI Generative AI Specialization", "NVIDIA Generative AI Certification", "LangChain Academy", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["Advanced Python", "Advanced SQL", "Machine Learning", "Deep Learning", "NLP", "Transformers", "Prompt Engineering", "LLM Development", "LangChain", "LangGraph", "LlamaIndex", "RAG", "AI Agents", "Vector Databases", "Fine-Tuning (LoRA/QLoRA)", "FastAPI", "Docker", "Azure AI / AWS Bedrock / Vertex AI", "Git & GitHub", "2,400+ Practice Problems Solved", "40+ Real-World LLM Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for LLM (Large Language Model) Engineer Roles"]
            }
        )

        # ----------------------------------------------------------------
        # 24. Prompt Engineer
        # ----------------------------------------------------------------
        seed_career(
            {
                "name": "Prompt Engineer",
                "slug": "prompt-engineer",
                "overview": "Career Category: Artificial Intelligence / Generative AI / LLM Applications | Difficulty: Beginner → Advanced | Learning Duration: 4–8 Months.",
                "india_salary": "Fresher: ₹8–15 LPA, Mid-Level: ₹15–30 LPA, Senior: ₹60 LPA–₹1 Cr+",
                "industry_demand": "Extremely High. Top Recruiters: OpenAI, Microsoft, Google, Anthropic, Meta, Amazon, NVIDIA, Adobe, Salesforce, Oracle, IBM, Deloitte, EY, Accenture, TCS, Infosys, Cognizant, Capgemini",
                "who_can_apply": ", ".join(branches) + ", Biotechnology Engineering, Mathematics & Computing, Data Science, Statistics"
            },
            {
                "title": "Prompt Engineer Complete Roadmap",
                "description": "Master the art and science of instructing AI to generate high-quality outputs using advanced prompting techniques.",
                "skills_matrix": {
                    "Programming": ["Python", "SQL", "JavaScript (Basics)"],
                    "AI Fundamentals": ["AI Basics", "Machine Learning Basics", "Deep Learning Basics", "NLP Basics", "Transformer Architecture", "LLM Fundamentals"],
                    "Prompt Engineering": ["Zero-shot", "One-shot", "Few-shot", "Chain of Thought (CoT)", "Tree of Thought (ToT)", "ReAct Prompting", "Self-Consistency Prompting", "Role Prompting", "Instruction Prompting", "Context Engineering", "Prompt Templates", "Structured Prompting", "Prompt Chaining", "Output Formatting", "JSON Mode", "Function Calling", "Structured Outputs"],
                    "LLMs": ["GPT Models", "Claude", "Gemini", "Llama", "Mistral", "Qwen", "DeepSeek", "Phi", "Gemma"],
                    "AI Frameworks & RAG": ["LangChain", "LangGraph", "LlamaIndex", "Semantic Kernel", "CrewAI", "AutoGen", "Embeddings", "Chunking", "Retrieval Strategies", "Vector Search", "Hybrid Search", "Context Optimization", "RAG Pipelines"],
                    "Databases & Vector DBs": ["Pinecone", "ChromaDB", "FAISS", "Weaviate", "Milvus", "Qdrant"],
                    "APIs & Deployment": ["OpenAI API", "Anthropic API", "Google Gemini API", "REST APIs", "FastAPI", "Flask", "Docker"],
                    "Cloud AI": ["Azure AI Foundry", "Azure OpenAI", "Amazon Bedrock", "Vertex AI", "Gemini API"],
                    "Soft Skills": ["Creative Thinking", "Analytical Thinking", "Technical Writing", "Communication", "Problem Solving", "Business Understanding", "Documentation"]
                },
                "learning_steps": [
                    {"phase": 1, "title": "Python & AI Basics", "duration": "3 Weeks", "learn": ["Python Basics", "SQL Basics", "AI Fundamentals", "NLP Basics"]},
                    {"phase": 2, "title": "Prompt Engineering Fundamentals", "duration": "4 Weeks", "learn": ["Prompt Design", "Prompt Patterns", "Zero-shot", "Few-shot", "Chain of Thought", "ReAct", "Prompt Templates"]},
                    {"phase": 3, "title": "LLM Applications", "duration": "4 Weeks", "learn": ["GPT", "Claude", "Gemini", "Llama", "Prompt Optimization", "Function Calling"]},
                    {"phase": 4, "title": "LangChain & AI Agents", "duration": "4 Weeks", "learn": ["LangChain", "LangGraph", "CrewAI", "AutoGen", "AI Agents", "Workflow Automation"]},
                    {"phase": 5, "title": "RAG & Vector Databases", "duration": "3 Weeks", "learn": ["RAG", "Embeddings", "Pinecone", "ChromaDB", "FAISS"]},
                    {"phase": 6, "title": "Deployment", "duration": "2 Weeks", "learn": ["FastAPI", "Flask", "Docker", "REST APIs"]},
                    {"phase": 7, "title": "Cloud AI", "duration": "2 Weeks", "learn": ["Azure OpenAI", "Amazon Bedrock", "Vertex AI"]},
                    {"phase": 8, "title": "Portfolio Development", "duration": "2 Weeks", "learn": ["GitHub Portfolio", "Prompt Library", "AI Portfolio Website", "ATS Resume", "LinkedIn Profile"]},
                    {"phase": 9, "title": "Interview Preparation", "duration": "2 Weeks", "learn": ["Prompt Engineering", "GPT Models", "LangChain", "RAG", "AI Agents", "Vector Databases", "HR", "AI Use Cases"]}
                ],
                "learning_plans": [
                    {"name": "Fast Track Plan", "duration": "4 Months", "daily_hours": "4 Hours"},
                    {"name": "Standard Plan", "duration": "6 Months", "daily_hours": "3 Hours"},
                    {"name": "Balanced Plan", "duration": "8 Months", "daily_hours": "2.5 Hours"},
                    {"name": "Flexible Plan", "duration": "12 Months", "daily_hours": "2 Hours"}
                ],
                "projects": {
                    "Beginner": ["AI Resume Generator", "AI Email Writer", "AI Story Generator", "AI Blog Writer", "AI Translator"],
                    "Intermediate": ["AI Customer Support Chatbot", "AI Content Generator", "AI Coding Assistant", "AI Learning Assistant", "AI Research Assistant"],
                    "Advanced": ["Enterprise Prompt Management Platform", "AI Multi-Agent Workflow", "AI Business Copilot", "AI HR Assistant", "AI Sales Assistant"],
                    "Industry-Level": ["Enterprise AI Knowledge Platform", "AI Legal Assistant", "AI Healthcare Copilot", "AI Financial Advisor", "AI Customer Success Platform", "AI Education Tutor", "AI Recruitment Assistant", "AI Software Engineering Copilot"]
                },
                "practice_questions": {
                    "Python": ["500 Coding Problems"],
                    "SQL": ["400 SQL Queries"],
                    "Prompt Engineering": ["500 Prompt Challenges"],
                    "LLM Applications": ["150 AI Use Cases"],
                    "LangChain": ["100 AI Workflows"],
                    "RAG": ["100 Practical Projects"],
                    "AI Agents": ["80 Automation Projects"],
                    "APIs": ["50 API Integrations"]
                },
                "certifications": ["Microsoft Azure AI Engineer Associate (AI-102)", "Google Generative AI Learning Path", "DeepLearning.AI Prompt Engineering", "DeepLearning.AI Generative AI Specialization", "LangChain Academy", "Hugging Face AI Course", "OpenAI API Developer Course", "Python Certification", "SQL Certification"],
                "readiness_checklist": ["Advanced Python", "SQL", "AI Fundamentals", "NLP Basics", "Prompt Engineering", "GPT / Claude / Gemini", "LangChain", "LangGraph", "RAG", "AI Agents", "Vector Databases", "FastAPI", "Docker", "Azure AI / AWS Bedrock / Vertex AI", "Git & GitHub", "Prompt Portfolio (500+ Prompts)", "1,880+ Practice Problems Solved", "35+ Real-World AI Projects Completed", "GitHub Portfolio Ready", "Portfolio Website Ready", "ATS Resume Created", "LinkedIn Optimized", "20 Mock Interviews Completed", "Ready to Apply for Prompt Engineer Roles"]
            }
        )

    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
