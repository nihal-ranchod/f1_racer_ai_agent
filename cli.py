#!/usr/bin/env python3
"""
F1 Racer AI Agent - Command Line Interface

Interactive CLI for the F1 AI Agent with configuration options and
all agent capabilities (Speak, Act, Think).

Author: F1 AI Agent Assessment
Date: 2025
"""

import sys
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import the F1 Agent and data
from f1_agent import F1Agent, create_f1_agent, MessageType, ContextState
from f1_data import F1_TEAMS, F1_CIRCUITS, SessionType

# Rich library for better CLI experience (optional)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None
    print("Rich library not available. Using basic CLI interface.")
    print("Install with: pip install rich")

class F1AgentCLI:
    """Command Line Interface for the F1 AI Agent"""
    
    def __init__(self):
        self.agent: Optional[F1Agent] = None
        self.configured = False
        
    def display_welcome(self):
        """Display welcome message and setup info"""
        if RICH_AVAILABLE:
            welcome_text = Text("🏎️  F1 Racer AI Agent", style="bold red")
            rprint(Panel(welcome_text, title="Welcome", border_style="blue"))
            rprint("[cyan]An AI agent that mimics Formula 1 racer persona and behavior[/cyan]\n")
        else:
            print("=" * 50)
            print("🏎️  F1 Racer AI Agent")
            print("=" * 50)
            print("An AI agent that mimics Formula 1 racer persona and behavior\n")
    
    def configure_agent(self) -> bool:
        """Configure the agent with driver and team information"""
        if RICH_AVAILABLE:
            rprint("[bold yellow]🔧 Agent Configuration[/bold yellow]\n")
        else:
            print("\n🔧 Agent Configuration")
            print("-" * 25)
        
        # Display available teams
        self.display_available_teams()
        
        # Get user input
        if RICH_AVAILABLE:
            driver_name = Prompt.ask("[green]Enter driver name[/green]", default="Alex Driver")
            team_key = Prompt.ask("[green]Enter team key[/green]", 
                                 choices=list(F1_TEAMS.keys()), 
                                 default="mclaren")
        else:
            driver_name = input("Enter driver name (default: Alex Driver): ").strip() or "Alex Driver"
            print("Available teams:", ", ".join(F1_TEAMS.keys()))
            team_key = input("Enter team key (default: mclaren): ").strip() or "mclaren"
            
            if team_key not in F1_TEAMS:
                print(f"Invalid team key. Using 'mclaren'.")
                team_key = "mclaren"
        
        # Create agent
        try:
            self.agent = create_f1_agent(driver_name, team_key)
            self.configured = True
            
            if RICH_AVAILABLE:
                rprint(f"[green]✅ Agent configured successfully![/green]")
                rprint(f"Driver: [bold]{driver_name}[/bold]")
                rprint(f"Team: [bold]{F1_TEAMS[team_key].name}[/bold]")
            else:
                print(f"✅ Agent configured successfully!")
                print(f"Driver: {driver_name}")
                print(f"Team: {F1_TEAMS[team_key].name}")
            
            # Optional: Set initial circuit
            self.configure_initial_context()
            return True
            
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error creating agent: {e}[/red]")
            else:
                print(f"❌ Error creating agent: {e}")
            return False
    
    def configure_initial_context(self):
        """Configure initial race weekend context"""
        if RICH_AVAILABLE:
            setup_context = Confirm.ask("Would you like to set up initial race weekend context?", default=True)
        else:
            response = input("Would you like to set up initial race weekend context? (y/N): ").strip().lower()
            setup_context = response in ['y', 'yes', '1', 'true']
        
        if setup_context:
            self.display_available_circuits()
            
            if RICH_AVAILABLE:
                circuit_key = Prompt.ask("[green]Select circuit[/green]", 
                                       choices=list(F1_CIRCUITS.keys()), 
                                       default="silverstone")
                weekend_type = Prompt.ask("[green]Weekend type[/green]", 
                                        choices=["standard_weekend", "sprint_weekend"],
                                        default="standard_weekend")
            else:
                print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:10]), "... (and more)")
                circuit_key = input("Select circuit (default: silverstone): ").strip() or "silverstone"
                if circuit_key not in F1_CIRCUITS:
                    circuit_key = "silverstone"
                
                print("Weekend types: standard_weekend, sprint_weekend")
                weekend_type = input("Weekend type (default: standard_weekend): ").strip() or "standard_weekend"
                if weekend_type not in ["standard_weekend", "sprint_weekend"]:
                    weekend_type = "standard_weekend"
            
            # Update agent context
            self.agent.think_update_context(
                current_circuit=circuit_key,
                weekend_type=weekend_type,
                current_state=ContextState.PRE_WEEKEND
            )
            
            circuit = F1_CIRCUITS[circuit_key]
            if RICH_AVAILABLE:
                rprint(f"[green]🏁 Context set to {circuit.name} ({circuit.country})[/green]")
            else:
                print(f"🏁 Context set to {circuit.name} ({circuit.country})")
    
    def display_available_teams(self):
        """Display available F1 teams"""
        if RICH_AVAILABLE:
            table = Table(title="Available F1 Teams (2025 Season)")
            table.add_column("Key", style="cyan")
            table.add_column("Team Name", style="white")
            table.add_column("Drivers", style="yellow")
            table.add_column("Engine", style="green")
            
            for key, team in F1_TEAMS.items():
                table.add_row(key, team.name, ", ".join(team.drivers), team.engine)
            
            console.print(table)
        else:
            print("\nAvailable F1 Teams (2025 Season):")
            print("-" * 60)
            for key, team in F1_TEAMS.items():
                print(f"{key:15} | {team.name:30} | {', '.join(team.drivers)}")
    
    def display_available_circuits(self):
        """Display available F1 circuits"""
        if RICH_AVAILABLE:
            rprint("[bold]Available Circuits (showing first 10):[/bold]")
            for i, (key, circuit) in enumerate(list(F1_CIRCUITS.items())[:10]):
                rprint(f"[cyan]{key}[/cyan]: {circuit.name} ({circuit.country})")
            rprint("[dim]...and more circuits available[/dim]")
        else:
            print("\nAvailable Circuits (showing first 10):")
            for i, (key, circuit) in enumerate(list(F1_CIRCUITS.items())[:10]):
                print(f"{key}: {circuit.name} ({circuit.country})")
            print("...and more circuits available")
    
    def display_main_menu(self):
        """Display the main menu options"""
        if RICH_AVAILABLE:
            menu_text = Text("Agent Capabilities", style="bold cyan")
            menu_panel = Panel(menu_text, border_style="blue")
            rprint(menu_panel)
            
            options = [
                ("1", "Generate Message", "(Speak)", "green"),
                ("2", "Post Status Update", "(Act)", "blue"),
                ("3", "Reply to Fan Comment", "(Act)", "blue"),
                ("4", "Like a Post", "(Act)", "blue"),
                ("5", "Mention Someone", "(Act)", "blue"),
                ("6", "Show Current Context", "(Think)", "magenta"),
                ("7", "Update Context", "(Think)", "magenta"),
                ("8", "Run Race Weekend Simulation", "(Full Simulation)", "yellow"),
                ("9", "Exit", "", "red")
            ]
            
            for num, action, category, color in options:
                rprint(f"[{color}]{num}. {action} {category}[/{color}]")
        else:
            print("\n" + "=" * 40)
            print("--- Agent Capabilities ---")
            print("=" * 40)
            print("1. Generate Message (Speak)")
            print("2. Post Status Update (Act)")
            print("3. Reply to Fan Comment (Act)")
            print("4. Like a Post (Act)")
            print("5. Mention Someone (Act)")
            print("6. Show Current Context (Think)")
            print("7. Update Context (Think)")
            print("8. Run Race Weekend Simulation")
            print("9. Exit")
    
    def handle_generate_message(self):
        """Handle generating a message (Speak capability)"""
        if RICH_AVAILABLE:
            rprint("[bold green]🎤 Generate Message (Speak)[/bold green]\n")
            
            message_types = ["post", "reply", "status_update", "mention"]
            msg_type = Prompt.ask("Message type", choices=message_types, default="post")
            custom_context = Prompt.ask("Additional context (optional)", default="")
        else:
            print("\n🎤 Generate Message (Speak)")
            print("-" * 30)
            print("Message types: post, reply, status_update, mention")
            msg_type = input("Message type (default: post): ").strip() or "post"
            custom_context = input("Additional context (optional): ").strip()
        
        try:
            message_type = MessageType(msg_type)
            context = custom_context if custom_context else None
            
            # Generate message
            message = self.agent.speak(message_type, context)
            
            if RICH_AVAILABLE:
                message_panel = Panel(f"[white]{message}[/white]", 
                                    title="Generated Message", 
                                    border_style="green")
                rprint(message_panel)
            else:
                print("\n📱 Generated Message:")
                print("-" * 30)
                print(f"'{message}'")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error generating message: {e}[/red]")
            else:
                print(f"❌ Error generating message: {e}")
    
    def handle_post_status(self):
        """Handle posting status update (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]📱 Post Status Update (Act)[/bold blue]\n")
            custom_content = Prompt.ask("Custom content (leave empty to auto-generate)", default="")
        else:
            print("\n📱 Post Status Update (Act)")
            print("-" * 30)
            custom_content = input("Custom content (leave empty to auto-generate): ").strip()
        
        try:
            content = custom_content if custom_content else None
            action = self.agent.act_post_status(content)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Status posted successfully![/green]")
                post_panel = Panel(f"[white]{action.content}[/white]", 
                                 title="Posted Content", 
                                 border_style="blue")
                rprint(post_panel)
                rprint(f"[dim]Engagement: {action.metadata.get('engagement', 'N/A')} interactions[/dim]")
            else:
                print("✅ Status posted successfully!")
                print(f"Content: '{action.content}'")
                print(f"Engagement: {action.metadata.get('engagement', 'N/A')} interactions")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting status: {e}[/red]")
            else:
                print(f"❌ Error posting status: {e}")
    
    def handle_reply_comment(self):
        """Handle replying to fan comment (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]💬 Reply to Fan Comment (Act)[/bold blue]\n")
            fan_comment = Prompt.ask("Enter the fan comment to reply to")
        else:
            print("\n💬 Reply to Fan Comment (Act)")
            print("-" * 30)
            fan_comment = input("Enter the fan comment to reply to: ").strip()
        
        if not fan_comment:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No comment provided[/yellow]")
            else:
                print("⚠️  No comment provided")
            return
        
        try:
            action = self.agent.act_reply_to_comment(fan_comment)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Reply posted successfully![/green]")
                rprint(f"[dim]Original comment:[/dim] [italic]{fan_comment}[/italic]")
                reply_panel = Panel(f"[white]{action.content}[/white]", 
                                  title="Your Reply", 
                                  border_style="blue")
                rprint(reply_panel)
                rprint(f"[dim]Detected sentiment: {action.metadata.get('original_sentiment', 'unknown')}[/dim]")
            else:
                print("✅ Reply posted successfully!")
                print(f"Original: '{fan_comment}'")
                print(f"Reply: '{action.content}'")
                print(f"Sentiment: {action.metadata.get('original_sentiment', 'unknown')}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting reply: {e}[/red]")
            else:
                print(f"❌ Error posting reply: {e}")
    
    def handle_like_post(self):
        """Handle liking a post (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]👍 Like a Post (Act)[/bold blue]\n")
            post_content = Prompt.ask("Enter the post content to like")
        else:
            print("\n👍 Like a Post (Act)")
            print("-" * 30)
            post_content = input("Enter the post content to like: ").strip()
        
        if not post_content:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No post content provided[/yellow]")
            else:
                print("⚠️  No post content provided")
            return
        
        try:
            action = self.agent.act_like_post(post_content)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Post liked successfully![/green]")
                rprint(f"[dim]Liked post:[/dim] [italic]{post_content[:100]}{'...' if len(post_content) > 100 else ''}[/italic]")
            else:
                print("✅ Post liked successfully!")
                print(f"Liked: '{post_content[:100]}{'...' if len(post_content) > 100 else ''}'")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error liking post: {e}[/red]")
            else:
                print(f"❌ Error liking post: {e}")
    
    def handle_mention_someone(self):
        """Handle mentioning someone (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]@️ Mention Someone (Act)[/bold blue]\n")
            person_name = Prompt.ask("Enter person name to mention")
            context = Prompt.ask("Mention context", default="general")
        else:
            print("\n@️ Mention Someone (Act)")
            print("-" * 30)
            person_name = input("Enter person name to mention: ").strip()
            context = input("Mention context (default: general): ").strip() or "general"
        
        if not person_name:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No person name provided[/yellow]")
            else:
                print("⚠️  No person name provided")
            return
        
        try:
            action = self.agent.act_mention_someone(person_name, context)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Mention posted successfully![/green]")
                mention_panel = Panel(f"[white]{action.content}[/white]", 
                                    title=f"Mentioning @{person_name}", 
                                    border_style="blue")
                rprint(mention_panel)
                rprint(f"[dim]Context: {action.metadata.get('mention_context', 'general')}[/dim]")
            else:
                print("✅ Mention posted successfully!")
                print(f"Content: '{action.content}'")
                print(f"Context: {action.metadata.get('mention_context', 'general')}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting mention: {e}[/red]")
            else:
                print(f"❌ Error posting mention: {e}")
    
    def handle_show_context(self):
        """Handle showing current context (Think capability)"""
        if RICH_AVAILABLE:
            rprint("[bold magenta]🧠 Show Current Context (Think)[/bold magenta]\n")
        else:
            print("\n🧠 Show Current Context (Think)")
            print("-" * 35)
        
        try:
            context = self.agent.think_show_context()
            
            if RICH_AVAILABLE:
                # Driver info
                driver_table = Table(title="Driver Information")
                driver_table.add_column("Property", style="cyan")
                driver_table.add_column("Value", style="white")
                
                for key, value in context["driver_info"].items():
                    driver_table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(driver_table)
                
                # Current situation
                situation_table = Table(title="Current Situation")
                situation_table.add_column("Property", style="cyan")
                situation_table.add_column("Value", style="white")
                
                for key, value in context["current_situation"].items():
                    situation_table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(situation_table)
                
                # Recent activity
                if context["recent_activity"]["last_result"]:
                    result = context["recent_activity"]["last_result"]
                    rprint(f"[yellow]Last Result:[/yellow] P{result['position']} - {result['best_time']} ({result['laps_completed']} laps)")
                
                if context["recent_activity"]["recent_incidents"]:
                    rprint(f"[red]Recent Incidents:[/red] {', '.join(context['recent_activity']['recent_incidents'])}")
                    
            else:
                print("Driver Information:")
                for key, value in context["driver_info"].items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
                
                print("\nCurrent Situation:")
                for key, value in context["current_situation"].items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
                
                print("\nRecent Activity:")
                for key, value in context["recent_activity"].items():
                    if value:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
                        
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error showing context: {e}[/red]")
            else:
                print(f"❌ Error showing context: {e}")
    
    def handle_update_context(self):
        """Handle updating context (Think capability)"""
        if RICH_AVAILABLE:
            rprint("[bold magenta]🔄 Update Context (Think)[/bold magenta]\n")
            
            # Show current context first
            current_context = self.agent.think_show_context()
            rprint(f"[dim]Current circuit: {current_context['current_situation']['circuit']}[/dim]")
            rprint(f"[dim]Current session: {current_context['current_situation']['session']}[/dim]")
            rprint(f"[dim]Current mood: {current_context['current_situation']['mood']}[/dim]\n")
            
            # Get updates
            new_circuit = Prompt.ask("New circuit", 
                                   choices=list(F1_CIRCUITS.keys()) + [""], 
                                   default="")
            
            new_session = Prompt.ask("New session", 
                                   choices=[s.value for s in SessionType] + [""], 
                                   default="")
            
            new_mood = Prompt.ask("New mood", 
                                choices=["ecstatic", "satisfied", "neutral", "disappointed", "frustrated", ""], 
                                default="")
        else:
            print("\n🔄 Update Context (Think)")
            print("-" * 30)
            
            # Show current values
            current_context = self.agent.think_show_context()
            print(f"Current circuit: {current_context['current_situation']['circuit']}")
            print(f"Current session: {current_context['current_situation']['session']}")
            print(f"Current mood: {current_context['current_situation']['mood']}")
            
            print("\nEnter new values (leave empty to keep current):")
            print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:5]), "... (and more)")
            new_circuit = input("New circuit: ").strip()
            
            print("Sessions: fp1, fp2, fp3, sprint_shootout, sprint_race, qualifying, race")
            new_session = input("New session: ").strip()
            
            print("Moods: ecstatic, satisfied, neutral, disappointed, frustrated")
            new_mood = input("New mood: ").strip()
        
        # Apply updates
        updates = {}
        if new_circuit and new_circuit in F1_CIRCUITS:
            updates["current_circuit"] = new_circuit
        if new_session:
            try:
                updates["current_session"] = SessionType(new_session)
            except ValueError:
                if RICH_AVAILABLE:
                    rprint(f"[yellow]⚠️  Invalid session type: {new_session}[/yellow]")
                else:
                    print(f"⚠️  Invalid session type: {new_session}")
        if new_mood:
            updates["mood"] = new_mood
        
        if updates:
            success = self.agent.think_update_context(**updates)
            if success:
                if RICH_AVAILABLE:
                    rprint("[green]✅ Context updated successfully![/green]")
                else:
                    print("✅ Context updated successfully!")
            else:
                if RICH_AVAILABLE:
                    rprint("[red]❌ Error updating context[/red]")
                else:
                    print("❌ Error updating context")
        else:
            if RICH_AVAILABLE:
                rprint("[yellow]ℹ️  No updates provided[/yellow]")
            else:
                print("ℹ️  No updates provided")
    
    def handle_race_simulation(self):
        """Handle running race weekend simulation"""
        if RICH_AVAILABLE:
            rprint("[bold yellow]🏁 Run Race Weekend Simulation[/bold yellow]\n")
            
            circuit_key = Prompt.ask("Select circuit for simulation", 
                                   choices=list(F1_CIRCUITS.keys()), 
                                   default=self.agent.context.current_circuit)
            
            weekend_type = Prompt.ask("Weekend type", 
                                    choices=["standard_weekend", "sprint_weekend"], 
                                    default="standard_weekend")
        else:
            print("\n🏁 Run Race Weekend Simulation")
            print("-" * 35)
            
            print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:10]), "... (and more)")
            current_circuit = self.agent.context.current_circuit
            circuit_key = input(f"Select circuit (default: {current_circuit}): ").strip() or current_circuit
            
            print("Weekend types: standard_weekend, sprint_weekend")
            weekend_type = input("Weekend type (default: standard_weekend): ").strip() or "standard_weekend"
        
        if circuit_key not in F1_CIRCUITS:
            circuit_key = self.agent.context.current_circuit
        
        try:
            if RICH_AVAILABLE:
                with console.status("[bold green]Running race weekend simulation...") as status:
                    results = self.agent.run_race_weekend_simulation(circuit_key, weekend_type)
            else:
                print("Running race weekend simulation...")
                results = self.agent.run_race_weekend_simulation(circuit_key, weekend_type)
            
            # Display results
            if RICH_AVAILABLE:
                simulation_panel = Panel(f"[white]{results['circuit']} - {results['weekend_type'].replace('_', ' ').title()}[/white]", 
                                       title="Weekend Simulation Results", 
                                       border_style="yellow")
                rprint(simulation_panel)
                
                # Session results
                for i, session in enumerate(results["sessions"]):
                    rprint(f"[cyan]{session['day']} - {session['session'].title()}:[/cyan]")
                    rprint(f"  Position: P{session['result']['position']}")
                    rprint(f"  Best Time: {session['result']['best_time']}")
                    rprint(f"  Message: [italic]{session['message']}[/italic]\n")
                
                final_panel = Panel(f"[white]{results['final_status']}[/white]", 
                                  title="Weekend Summary", 
                                  border_style="green")
                rprint(final_panel)
            else:
                print(f"\n🏁 Weekend Simulation: {results['circuit']} - {results['weekend_type'].replace('_', ' ').title()}")
                print("=" * 60)
                
                for session in results["sessions"]:
                    print(f"\n{session['day']} - {session['session'].title()}:")
                    print(f"  Position: P{session['result']['position']}")
                    print(f"  Best Time: {session['result']['best_time']}")
                    print(f"  Message: '{session['message']}'")
                
                print(f"\n🏆 Weekend Summary: {results['final_status']}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error running simulation: {e}[/red]")
            else:
                print(f"❌ Error running simulation: {e}")
    
    def run(self):
        """Main CLI loop"""
        self.display_welcome()
        
        # Configure agent first
        if not self.configure_agent():
            if RICH_AVAILABLE:
                rprint("[red]❌ Agent configuration failed. Exiting.[/red]")
            else:
                print("❌ Agent configuration failed. Exiting.")
            sys.exit(1)
        
        # Main menu loop
        while True:
            try:
                self.display_main_menu()
                
                if RICH_AVAILABLE:
                    choice = Prompt.ask("\n[bold]Select option[/bold]", 
                                      choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
                else:
                    choice = input("\nSelect option (1-9): ").strip()
                
                if choice == "1":
                    self.handle_generate_message()
                elif choice == "2":
                    self.handle_post_status()
                elif choice == "3":
                    self.handle_reply_comment()
                elif choice == "4":
                    self.handle_like_post()
                elif choice == "5":
                    self.handle_mention_someone()
                elif choice == "6":
                    self.handle_show_context()
                elif choice == "7":
                    self.handle_update_context()
                elif choice == "8":
                    self.handle_race_simulation()
                elif choice == "9":
                    if RICH_AVAILABLE:
                        rprint("[yellow]👋 Thanks for using F1 Racer AI Agent![/yellow]")
                    else:
                        print("👋 Thanks for using F1 Racer AI Agent!")
                    break
                else:
                    if RICH_AVAILABLE:
                        rprint("[red]❌ Invalid choice. Please select 1-9.[/red]")
                    else:
                        print("❌ Invalid choice. Please select 1-9.")
                
                # Pause between operations
                if RICH_AVAILABLE:
                    input("\n[dim]Press Enter to continue...[/dim]")
                else:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                if RICH_AVAILABLE:
                    rprint("\n[yellow]👋 Goodbye![/yellow]")
                else:
                    print("\n👋 Goodbye!")
                break
            except Exception as e:
                if RICH_AVAILABLE:
                    rprint(f"[red]❌ Unexpected error: {e}[/red]")
                else:
                    print(f"❌ Unexpected error: {e}")

def main():
    """Entry point for the CLI application"""
    cli = F1AgentCLI()
    cli.run()

if __name__ == "__main__":
    main()