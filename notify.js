function find_today_staff() {
    // Main sheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Ed Assignments, Fall 2023");
    
    // Generated assignment, easier to work with to just get the names and dates
    var generated_assignment = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("generated_assignment");
  
    // Get current date and list of dates and names in the generated assignment
    var currentDate = new Date();
    var dates = generated_assignment.getRange("A:A").getValues(); 
    var names = generated_assignment.getRange("B:D").getValues();
  
    // Get the name to email conversion columns in the main sheet
    var name_email = sheet.getRange("F:G").getValues();
  
  
    // Look through the generated assignment to find the names of staff on duty today
    let staff_today = [];
    for (var i = 0; i < dates.length; i++) {
      if (dates[i][0] instanceof Date && dates[i][0].toDateString() === currentDate.toDateString()) {
        // Current date found in the sheet, return the row number
        for (var col = 0; col < 3; col++) {
          staff_today.push(names[i][col]);
          console.log(names[i][col])
        }
      }
    }
  
    if (staff_today.length === 0) {
      console.log("Current date not in the assignment.")  
      return "Current date not in the assignment.";
    }
  
    // Logging staff on duty today
    console.log(staff_today);
    
    // Look through the conversion columns and find the email for each staff member on duty
    let emails = [];
    staff_today.forEach((staff) => {
  
      // If staff member assigned
      if (staff) {
        
        // Look through conversion columns, if left column (name column) match, push right column (email column)
        name_email.forEach( (row)  => {
          if (row[0] == staff) {
            emails.push(row[1]);
          }
        })
      }
    })
  
    // Logging the emails of staff on duty today
    console.log(emails);
  
  
    // Email configuration
    var subject = "CS50 Ed Reminder";
    var message = `Hi all,
  
  This is an automated email to remind you that you are on Ed duty for CS50 today. Please review the guidance for monitoring Ed here: https://cs50.tf/college/2023/fall/ed/.
  
  While this is automated to make my life easier, you can reply to this email or Slack me to ask any questions or if you need help. If you need to swap, please post on Slack and we will try to help.
  
  Best,
  Andrew
    `;
  
    let html_message =  `Hi all,
  
  This is an automated email to remind you that you are on Ed duty for CS50 today. <a href="https://cs50.tf/college/2023/fall/ed/">Please review the guidance for monitoring Ed here</a>.
  
  While this is automated to make my life easier, you can reply to this email or Slack me to ask any questions or if you need help. If you need to swap, please post on Slack and we will try to help.
  
  Best,
  Andrew
    `;
  
    // If we have email addresses for staff, send email
    if (emails.length != 0) {
      console.log(emails);
      MailApp.sendEmail({
        to: emails.join(","),
        subject: subject, 
        body: message,
        htmlbody: message
      });
        
      console.log("email sent, recipients: " + emails.join(","));
    }
  }
  