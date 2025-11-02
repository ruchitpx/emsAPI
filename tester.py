import requests
import json
import os
import sys
from datetime import datetime, timedelta

class InteractiveEventManagementTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.tokens = {}
        self.created_events = []
        self.created_rsvps = []
        self.created_reviews = []
        self.current_user = "organizer"
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("🎪 EVENT MANAGEMENT SYSTEM - INTERACTIVE API TESTER")
        print("=" * 60)
    
    def print_response(self, response, endpoint):
        """Helper method to print response details"""
        print(f"\n{'='*60}")
        print(f"📡 Endpoint: {endpoint}")
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        
        if response.status_code >= 400:
            print("❌ Response Body:")
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)
        else:
            print("✅ Success!")
            try:
                result = response.json()
                if isinstance(result, list):
                    print(f"📄 Items: {len(result)}")
                    print(json.dumps(result, indent=2))
                elif isinstance(result, dict) and 'results' in result:
                    print(f"📄 Total: {result.get('count', 'N/A')} items")
                    print(f"📄 Page: {len(result.get('results', []))} items")
                    if len(result.get('results', [])) <= 3:
                        print(json.dumps(result, indent=2))
                    else:
                        print("📋 (Response too large, showing first 3 items)")
                        result['results'] = result['results'][:3]
                        print(json.dumps(result, indent=2))
                else:
                    print(json.dumps(result, indent=2))
            except:
                print("📝 Response: (No JSON content)")
        
        print('=' * 60)
        input("\nPress Enter to continue...")
    
    def get_auth_headers(self, user_type=None):
        """Get authorization headers for a user"""
        user = user_type or self.current_user
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.tokens.get(user, {}).get('access', '')}"
        }
    
    def ensure_authentication(self):
        """Ensure we have valid tokens"""
        if not self.tokens.get("organizer") or not self.tokens.get("attendee"):
            print("🔐 Authentication required...")
            self.authenticate_users()
    
    def authenticate_users(self):
        """Authenticate both test users"""
        test_users = {
            "organizer": {"username": "tom", "password": "tom@1234"},
            "attendee": {"username": "jerry", "password": "jerry@1234"}
        }
        
        for user_type, credentials in test_users.items():
            print(f"Authenticating {user_type}...")
            response = requests.post(
                f"{self.base_url}/api/auth/token/",
                json=credentials
            )
            
            if response.status_code == 200:
                self.tokens[user_type] = response.json()
                print(f"✅ {user_type.capitalize()} authenticated successfully")
            else:
                print(f"❌ Failed to authenticate {user_type}")
                print(f"Error: {response.status_code} - {response.text}")
    
    def switch_user(self):
        """Switch between organizer and attendee"""
        print("\n👤 Current User:", self.current_user)
        print("1. Organizer (tom)")
        print("2. Attendee (jerry)")
        choice = input("Select user (1-2): ").strip()
        
        if choice == "1":
            self.current_user = "organizer"
            print("✅ Switched to Organizer")
        elif choice == "2":
            self.current_user = "attendee"
            print("✅ Switched to Attendee")
        else:
            print("❌ Invalid choice")
    
    # 1. Authentication Endpoints
    def test_1_1_get_token(self):
        """1.1 Get JWT Token"""
        print("\n🔐 1.1 - Get JWT Token")
        username = input("Username (default: tom): ").strip() or "tom"
        password = input("Password (default: tom@1234): ").strip() or "tom@1234"
        
        response = requests.post(
            f"{self.base_url}/api/auth/token/",
            json={"username": username, "password": password}
        )
        self.print_response(response, "POST /api/auth/token/")
        
        if response.status_code == 200:
            token_data = response.json()
            user_type = "organizer" if username == "tom" else "attendee"
            self.tokens[user_type] = token_data
            print(f"✅ Token stored for {user_type}")
    
    def test_1_2_refresh_token(self):
        """1.2 Refresh JWT Token"""
        print("\n🔄 1.2 - Refresh JWT Token")
        
        if not self.tokens.get(self.current_user):
            print("❌ No token available. Please authenticate first.")
            return
        
        refresh_token = self.tokens[self.current_user]["refresh"]
        response = requests.post(
            f"{self.base_url}/api/auth/token/refresh/",
            json={"refresh": refresh_token}
        )
        self.print_response(response, "POST /api/auth/token/refresh/")
        
        if response.status_code == 200:
            self.tokens[self.current_user]["access"] = response.json()["access"]
            print("✅ Token refreshed successfully!")
    
    # 2. Events Endpoints
    def test_2_1_list_events(self):
        """2.1 List All Events"""
        print("\n📋 2.1 - List All Events")
        
        # Get query parameters
        print("\nOptional query parameters:")
        search = input("Search term (press Enter to skip): ").strip()
        is_public = input("Is public (true/false, press Enter to skip): ").strip()
        ordering = input("Order by (-created_at, start_time, etc.): ").strip() or "-created_at"
        
        # Build URL with query parameters
        url = f"{self.base_url}/api/events/"
        params = []
        if search:
            params.append(f"search={search}")
        if is_public:
            params.append(f"is_public={is_public}")
        if ordering:
            params.append(f"ordering={ordering}")
        
        if params:
            url += "?" + "&".join(params)
        
        response = requests.get(url)
        self.print_response(response, f"GET {url}")
    
    def test_2_2_create_event(self):
        """2.2 Create New Event"""
        print("\n🆕 2.2 - Create New Event")
        self.ensure_authentication()
        
        # Default event data
        default_start = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT10:00:00Z")
        default_end = (datetime.now() + timedelta(days=30, hours=4)).strftime("%Y-%m-%dT14:00:00Z")
        
        print("\nEnter event details (press Enter for defaults):")
        title = input(f"Title (default: 'Tech Conference 2025'): ").strip() or "Tech Conference 2025"
        description = input(f"Description (default: 'Annual tech conference'): ").strip() or "Annual tech conference"
        location = input(f"Location (default: 'Convention Center'): ").strip() or "Convention Center"
        start_time = input(f"Start time (default: {default_start}): ").strip() or default_start
        end_time = input(f"End time (default: {default_end}): ").strip() or default_end
        is_public = input(f"Is public (true/false, default: true): ").strip().lower() or "true"
        
        event_data = {
            "title": title,
            "description": description,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
            "is_public": is_public == "true"
        }
        
        response = requests.post(
            f"{self.base_url}/api/events/",
            json=event_data,
            headers=self.get_auth_headers("organizer")
        )
        self.print_response(response, "POST /api/events/")
        
        if response.status_code == 201:
            event_id = response.json()["id"]
            self.created_events.append(event_id)
            print(f"✅ Event created with ID: {event_id}")
    
    def test_2_3_get_event_details(self):
        """2.3 Get Event Details"""
        print("\n📄 2.3 - Get Event Details")
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        response = requests.get(f"{self.base_url}/api/events/{event_id}/")
        self.print_response(response, f"GET /api/events/{event_id}/")
    
    def test_2_4_update_event(self):
        """2.4 Update Event"""
        print("\n✏️ 2.4 - Update Event")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID to update: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        # First get current event data
        response = requests.get(f"{self.base_url}/api/events/{event_id}/")
        if response.status_code != 200:
            print("❌ Cannot fetch event details")
            return
        
        current_event = response.json()
        print(f"\nCurrent event: {current_event['title']}")
        
        print("\nEnter new values (press Enter to keep current):")
        title = input(f"Title [{current_event['title']}]: ").strip() or current_event['title']
        description = input(f"Description [{current_event['description']}]: ").strip() or current_event['description']
        location = input(f"Location [{current_event['location']}]: ").strip() or current_event['location']
        
        update_data = {
            "title": title,
            "description": description,
            "location": location,
            "start_time": current_event['start_time'],
            "end_time": current_event['end_time'],
            "is_public": current_event['is_public']
        }
        
        response = requests.put(
            f"{self.base_url}/api/events/{event_id}/",
            json=update_data,
            headers=self.get_auth_headers("organizer")
        )
        self.print_response(response, f"PUT /api/events/{event_id}/")
    
    def test_2_5_delete_event(self):
        """2.5 Delete Event"""
        print("\n🗑️ 2.5 - Delete Event")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID to delete: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        confirm = input(f"⚠️  Are you sure you want to delete event {event_id}? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Deletion cancelled")
            return
        
        response = requests.delete(
            f"{self.base_url}/api/events/{event_id}/",
            headers=self.get_auth_headers("organizer")
        )
        
        if response.status_code == 204:
            print("✅ Event deleted successfully")
            if event_id in self.created_events:
                self.created_events.remove(event_id)
        else:
            print(f"❌ Failed to delete event: {response.status_code}")
        
        input("\nPress Enter to continue...")
    
    def test_2_6_rsvp_to_event(self):
        """2.6 RSVP to Event"""
        print("\n📝 2.6 - RSVP to Event")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        print("\nRSVP Status Options:")
        print("1. Going")
        print("2. Maybe") 
        print("3. Not Going")
        
        status_choice = input("Select status (1-3): ").strip()
        status_map = {"1": "Going", "2": "Maybe", "3": "Not Going"}
        status = status_map.get(status_choice, "Going")
        
        response = requests.post(
            f"{self.base_url}/api/events/{event_id}/rsvp/",
            json={"status": status},
            headers=self.get_auth_headers()
        )
        self.print_response(response, f"POST /api/events/{event_id}/rsvp/")
        
        if response.status_code == 200:
            rsvp_data = response.json()
            self.created_rsvps.append(rsvp_data["id"])
            print(f"✅ RSVP created with ID: {rsvp_data['id']}")
    
    def test_2_7_get_event_reviews(self):
        """2.7 Get Event Reviews"""
        print("\n⭐ 2.7 - Get Event Reviews")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        response = requests.get(
            f"{self.base_url}/api/events/{event_id}/reviews/",
            headers=self.get_auth_headers()
        )
        self.print_response(response, f"GET /api/events/{event_id}/reviews/")
    
    # 3. RSVP Endpoints
    def test_3_1_get_users_rsvps(self):
        """3.1 Get User's RSVPs"""
        print("\n📋 3.1 - Get User's RSVPs")
        self.ensure_authentication()
        
        response = requests.get(
            f"{self.base_url}/api/rsvps/",
            headers=self.get_auth_headers()
        )
        self.print_response(response, "GET /api/rsvps/")
    
    def test_3_2_create_rsvp(self):
        """3.2 Create RSVP"""
        print("\n🆕 3.2 - Create RSVP")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        print("\nRSVP Status Options:")
        print("1. Going")
        print("2. Maybe")
        print("3. Not Going")
        
        status_choice = input("Select status (1-3): ").strip()
        status_map = {"1": "Going", "2": "Maybe", "3": "Not Going"}
        status = status_map.get(status_choice, "Going")
        
        rsvp_data = {
            "event": event_id,
            "status": status
        }
        
        response = requests.post(
            f"{self.base_url}/api/rsvps/",
            json=rsvp_data,
            headers=self.get_auth_headers()
        )
        self.print_response(response, "POST /api/rsvps/")
        
        if response.status_code in [200, 201]:
            rsvp_data = response.json()
            self.created_rsvps.append(rsvp_data["id"])
            print(f"✅ RSVP created/updated with ID: {rsvp_data['id']}")
    
    def test_3_3_update_rsvp(self):
        """3.3 Update RSVP"""
        print("\n✏️ 3.3 - Update RSVP")
        self.ensure_authentication()
        
        # First get user's RSVPs to show available options
        response = requests.get(
            f"{self.base_url}/api/rsvps/",
            headers=self.get_auth_headers()
        )
        
        if response.status_code == 200:
            rsvps = response.json().get('results', [])
            if rsvps:
                print("\nYour RSVPs:")
                for rsvp in rsvps:
                    print(f"ID: {rsvp['id']} - Event: {rsvp['event']['title']} - Status: {rsvp['status']}")
            else:
                print("❌ No RSVPs found")
                return
        
        rsvp_id = input("\nEnter RSVP ID to update: ").strip()
        if not rsvp_id:
            print("❌ RSVP ID is required")
            return
        
        print("\nNew Status Options:")
        print("1. Going")
        print("2. Maybe")
        print("3. Not Going")
        
        status_choice = input("Select new status (1-3): ").strip()
        status_map = {"1": "Going", "2": "Maybe", "3": "Not Going"}
        new_status = status_map.get(status_choice, "Going")
        
        response = requests.put(
            f"{self.base_url}/api/rsvps/{rsvp_id}/",
            json={"status": new_status},
            headers=self.get_auth_headers()
        )
        self.print_response(response, f"PUT /api/rsvps/{rsvp_id}/")
    
    # 4. Reviews Endpoints
    def test_4_1_get_users_reviews(self):
        """4.1 Get User's Reviews"""
        print("\n📋 4.1 - Get User's Reviews")
        self.ensure_authentication()
        
        response = requests.get(
            f"{self.base_url}/api/reviews/",
            headers=self.get_auth_headers()
        )
        self.print_response(response, "GET /api/reviews/")
    
    def test_4_2_create_review(self):
        """4.2 Create Review"""
        print("\n🆕 4.2 - Create Review")
        self.ensure_authentication()
        
        if self.created_events:
            print(f"Available event IDs: {self.created_events}")
        
        event_id = input("Enter event ID: ").strip()
        if not event_id:
            print("❌ Event ID is required")
            return
        
        rating = input("Rating (1-5): ").strip()
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            print("❌ Rating must be between 1 and 5")
            return
        
        comment = input("Comment (optional): ").strip()
        
        review_data = {
            "event": event_id,
            "rating": int(rating),
            "comment": comment
        }
        
        response = requests.post(
            f"{self.base_url}/api/reviews/",
            json=review_data,
            headers=self.get_auth_headers()
        )
        self.print_response(response, "POST /api/reviews/")
        
        if response.status_code == 201:
            review_data = response.json()
            self.created_reviews.append(review_data["id"])
            print(f"✅ Review created with ID: {review_data['id']}")
    
    def show_status(self):
        """Show current test status"""
        print("\n📊 CURRENT TEST STATUS")
        print("=" * 40)
        print(f"👤 Current User: {self.current_user}")
        print(f"🔐 Tokens: {'✅ Available' if self.tokens else '❌ Not available'}")
        print(f"🎪 Created Events: {len(self.created_events)} - IDs: {self.created_events}")
        print(f"📝 Created RSVPs: {len(self.created_rsvps)} - IDs: {self.created_rsvps}")
        print(f"⭐ Created Reviews: {len(self.created_reviews)} - IDs: {self.created_reviews}")
        print("=" * 40)
        input("\nPress Enter to continue...")
    
    def run_complete_test_suite(self):
        """Run all tests in sequence"""
        print("\n🚀 RUNNING COMPLETE TEST SUITE")
        print("This will execute all API tests in sequence...")
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            return
        
        tests = [
            ("1.1 Get JWT Token", self.test_1_1_get_token),
            ("2.2 Create Event", self.test_2_2_create_event),
            ("2.6 RSVP to Event", self.test_2_6_rsvp_to_event),
            ("4.2 Create Review", self.test_4_2_create_review),
            ("3.1 Get User's RSVPs", self.test_3_1_get_users_rsvps),
            ("4.1 Get User's Reviews", self.test_4_1_get_users_reviews),
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'='*50}")
            print(f"Running: {test_name}")
            print('='*50)
            try:
                test_func()
            except Exception as e:
                print(f"❌ Error in {test_name}: {e}")
        
        print("\n🎉 COMPLETE TEST SUITE FINISHED!")
        self.show_status()
    
    def show_menu(self):
        """Display the main menu"""
        self.clear_screen()
        self.print_header()
        
        print("🔐 AUTHENTICATION ENDPOINTS")
        print("1.1 - Get JWT Token")
        print("1.2 - Refresh JWT Token")
        print("")
        
        print("🎪 EVENTS ENDPOINTS") 
        print("2.1 - List All Events")
        print("2.2 - Create New Event")
        print("2.3 - Get Event Details")
        print("2.4 - Update Event")
        print("2.5 - Delete Event")
        print("2.6 - RSVP to Event")
        print("2.7 - Get Event Reviews")
        print("")
        
        print("📝 RSVP ENDPOINTS")
        print("3.1 - Get User's RSVPs")
        print("3.2 - Create RSVP")
        print("3.3 - Update RSVP")
        print("")
        
        print("⭐ REVIEWS ENDPOINTS")
        print("4.1 - Get User's Reviews")
        print("4.2 - Create Review")
        print("")
        
        print("🛠️ UTILITIES")
        print("switch  - Switch User (Current: " + self.current_user + ")")
        print("status - Show Test Status")
        print("all - Run Complete Test Suite")
        print("quit  - Quit")
        print("")
        
        print("=" * 60)
    
    def run(self):
        """Main application loop"""
        # Auto-authenticate on start
        self.authenticate_users()
        
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q':
                print("👋 Goodbye!")
                break
            elif choice == 's':
                self.switch_user()
            elif choice == 'status':
                self.show_status()
            elif choice == 'all':
                self.run_complete_test_suite()
            else:
                self.execute_test(choice)
    
    def execute_test(self, choice):
        """Execute test based on choice"""
        test_map = {
            "1.1": self.test_1_1_get_token,
            "1.2": self.test_1_2_refresh_token,
            "2.1": self.test_2_1_list_events,
            "2.2": self.test_2_2_create_event,
            "2.3": self.test_2_3_get_event_details,
            "2.4": self.test_2_4_update_event,
            "2.5": self.test_2_5_delete_event,
            "2.6": self.test_2_6_rsvp_to_event,
            "2.7": self.test_2_7_get_event_reviews,
            "3.1": self.test_3_1_get_users_rsvps,
            "3.2": self.test_3_2_create_rsvp,
            "3.3": self.test_3_3_update_rsvp,
            "4.1": self.test_4_1_get_users_reviews,
            "4.2": self.test_4_2_create_review,
        }
        
        if choice in test_map:
            try:
                test_map[choice]()
            except Exception as e:
                print(f"❌ Error executing test: {e}")
                input("Press Enter to continue...")
        else:
            print("❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")

# Run the interactive tester
if __name__ == "__main__":
    try:
        tester = InteractiveEventManagementTester()
        tester.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")