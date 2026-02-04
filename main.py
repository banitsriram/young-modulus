"""
Young's Modulus Calculator for Rod Materials
This program calculates Young's modulus for thin sheet-like rods
based on bending experiments with different materials.
"""

import math

# Material properties database (Young's Modulus in GPa)
MATERIAL_DATABASE = {
    "iron": {
        "name": "Iron",
        "youngs_modulus": 210,  # GPa
        "density": 7.87  # g/cm³
    },
    "steel": {
        "name": "Steel (Mild)",
        "youngs_modulus": 200,  # GPa
        "density": 7.85  # g/cm³
    },
    "stainless_steel": {
        "name": "Stainless Steel",
        "youngs_modulus": 190,  # GPa
        "density": 8.00  # g/cm³
    },
    "aluminum": {
        "name": "Aluminum",
        "youngs_modulus": 69,  # GPa
        "density": 2.70  # g/cm³
    },
    "copper": {
        "name": "Copper",
        "youngs_modulus": 130,  # GPa
        "density": 8.96  # g/cm³
    },
    "brass": {
        "name": "Brass",
        "youngs_modulus": 100,  # GPa
        "density": 8.50  # g/cm³
    },
    "oak_wood": {
        "name": "Oak Wood",
        "youngs_modulus": 11,  # GPa
        "density": 0.75  # g/cm³
    },
    "pine_wood": {
        "name": "Pine Wood",
        "youngs_modulus": 9,  # GPa
        "density": 0.55  # g/cm³
    },
    "teak_wood": {
        "name": "Teak Wood",
        "youngs_modulus": 12,  # GPa
        "density": 0.65  # g/cm³
    },
    "bamboo": {
        "name": "Bamboo",
        "youngs_modulus": 20,  # GPa
        "density": 0.60  # g/cm³
    },
    "plywood": {
        "name": "Plywood",
        "youngs_modulus": 6,  # GPa
        "density": 0.55  # g/cm³
    },
    "pvc": {
        "name": "PVC",
        "youngs_modulus": 3,  # GPa
        "density": 1.40  # g/cm³
    },
    "acrylic": {
        "name": "Acrylic",
        "youngs_modulus": 3.2,  # GPa
        "density": 1.18  # g/cm³
    }
}


def display_materials():
    """Display available materials in the database"""
    print("\n" + "="*60)
    print("AVAILABLE MATERIALS IN DATABASE")
    print("="*60)
    for i, (key, material) in enumerate(MATERIAL_DATABASE.items(), 1):
        print(f"{i}. {material['name']:<20} - Young's Modulus: {material['youngs_modulus']} GPa")
    print("="*60)


def get_material_choice():
    """Get material selection from user"""
    display_materials()
    print("\nEnter the number corresponding to your material:")
    
    while True:
        try:
            choice = int(input("Your choice: "))
            if 1 <= choice <= len(MATERIAL_DATABASE):
                material_key = list(MATERIAL_DATABASE.keys())[choice - 1]
                return material_key, MATERIAL_DATABASE[material_key]
            else:
                print(f"Please enter a number between 1 and {len(MATERIAL_DATABASE)}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_dimensions():
    """Get rod dimensions from user"""
    print("\n" + "="*60)
    print("ENTER ROD DIMENSIONS")
    print("="*60)
    
    while True:
        try:
            length = float(input("Length of rod (in cm): "))
            breadth = float(input("Breadth of rod (in cm): "))
            width = float(input("Width/Thickness of rod (in cm): "))
            
            if length <= 0 or breadth <= 0 or width <= 0:
                print("All dimensions must be positive values. Please try again.")
                continue
            
            return length, breadth, width
        except ValueError:
            print("Invalid input. Please enter numerical values.")


def get_bending_type():
    """Get bending type from user"""
    print("\n" + "="*60)
    print("SELECT BENDING TYPE")
    print("="*60)
    print("1. Uniform Bending (Load distributed uniformly)")
    print("2. Non-Uniform Bending (Point load at center)")
    
    while True:
        try:
            choice = int(input("\nYour choice (1 or 2): "))
            if choice in [1, 2]:
                return choice
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")


def get_readings():
    """Get number of readings and weight measurements"""
    print("\n" + "="*60)
    print("MEASUREMENT READINGS")
    print("="*60)
    
    while True:
        try:
            num_readings = int(input("How many readings do you want to take? "))
            if num_readings <= 0:
                print("Please enter a positive number of readings.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        try:
            weight_increment = float(input("Weight added at each reading (in grams): "))
            if weight_increment <= 0:
                print("Weight must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value.")
    
    # Collect depression/elevation measurements
    readings = []
    print("\nEnter the depression/elevation at each reading (in cm):")
    print("(Positive for depression/downward, Negative for elevation/upward)")
    
    for i in range(num_readings):
        while True:
            try:
                weight = weight_increment * (i + 1)
                depression = float(input(f"Reading {i+1} (Weight: {weight} g): "))
                readings.append({
                    "reading_num": i + 1,
                    "weight": weight,
                    "depression": depression
                })
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
    
    return readings, weight_increment


def calculate_moment_of_inertia(breadth, width):
    """
    Calculate moment of inertia for rectangular cross-section
    I = (breadth * width³) / 12
    
    Args:
        breadth: breadth in cm
        width: thickness in cm
    
    Returns:
        Moment of inertia in cm⁴
    """
    return (breadth * width**3) / 12


def calculate_youngs_modulus_uniform(length, breadth, width, readings):
    """
    Calculate Young's modulus for uniform bending
    
    For uniform bending: Y = (M * L²) / (8 * I * δ)
    where M = moment, L = length, I = moment of inertia, δ = depression
    
    Args:
        length: length in cm
        breadth: breadth in cm
        width: thickness in cm
        readings: list of measurement readings
    
    Returns:
        Average Young's modulus in GPa
    """
    I = calculate_moment_of_inertia(breadth, width)
    youngs_moduli = []
    
    for reading in readings:
        weight_kg = reading["weight"] / 1000  # Convert grams to kg
        force_N = weight_kg * 9.81  # Force in Newtons
        depression_m = reading["depression"] / 100  # Convert cm to meters
        length_m = length / 100  # Convert cm to meters
        I_m4 = I / 100000000  # Convert cm⁴ to m⁴
        
        if depression_m != 0:
            # For uniform load: Y = (5 * w * L⁴) / (384 * I * δ)
            # where w = load per unit length = Force/Length
            w = force_N / length_m
            Y = (5 * w * length_m**4) / (384 * I_m4 * abs(depression_m))
            Y_GPa = Y / 1e9  # Convert Pa to GPa
            youngs_moduli.append(Y_GPa)
    
    return sum(youngs_moduli) / len(youngs_moduli) if youngs_moduli else 0


def calculate_youngs_modulus_nonuniform(length, breadth, width, readings):
    """
    Calculate Young's modulus for non-uniform bending (point load at center)
    
    For point load at center: Y = (W * L³) / (48 * I * δ)
    
    Args:
        length: length in cm
        breadth: breadth in cm
        width: thickness in cm
        readings: list of measurement readings
    
    Returns:
        Average Young's modulus in GPa
    """
    I = calculate_moment_of_inertia(breadth, width)
    youngs_moduli = []
    
    for reading in readings:
        weight_kg = reading["weight"] / 1000  # Convert grams to kg
        force_N = weight_kg * 9.81  # Force in Newtons
        depression_m = reading["depression"] / 100  # Convert cm to meters
        length_m = length / 100  # Convert cm to meters
        I_m4 = I / 100000000  # Convert cm⁴ to m⁴
        
        if depression_m != 0:
            # For point load at center: Y = (W * L³) / (48 * I * δ)
            Y = (force_N * length_m**3) / (48 * I_m4 * abs(depression_m))
            Y_GPa = Y / 1e9  # Convert Pa to GPa
            youngs_moduli.append(Y_GPa)
    
    return sum(youngs_moduli) / len(youngs_moduli) if youngs_moduli else 0


def display_results(material_key, material, length, breadth, width, 
                   bending_type, readings, calculated_modulus):
    """Display comprehensive results in a systematic table"""
    print("\n" + "="*80)
    print("YOUNG'S MODULUS CALCULATION RESULTS")
    print("="*80)
    
    # Material and Rod Information
    print("\nMATERIAL INFORMATION:")
    print(f"  Material: {material['name']}")
    print(f"  Expected Young's Modulus: {material['youngs_modulus']} GPa")
    print(f"  Density: {material['density']} g/cm³")
    
    print("\nROD DIMENSIONS:")
    print(f"  Length: {length} cm")
    print(f"  Breadth: {breadth} cm")
    print(f"  Width/Thickness: {width} cm")
    
    print("\nBENDING TYPE:")
    bending_name = "Uniform Bending" if bending_type == 1 else "Non-Uniform Bending (Point Load)"
    print(f"  {bending_name}")
    
    # Calculate moment of inertia
    I = calculate_moment_of_inertia(breadth, width)
    print(f"\nMOMENT OF INERTIA: {I:.6f} cm⁴")
    
    # Readings Table
    print("\n" + "-"*80)
    print("MEASUREMENT READINGS")
    print("-"*80)
    print(f"{'Reading':<10} {'Weight (g)':<15} {'Depression (cm)':<20} {'Individual Y (GPa)':<20}")
    print("-"*80)
    
    # Calculate individual Young's modulus for each reading
    for reading in readings:
        weight_kg = reading["weight"] / 1000
        force_N = weight_kg * 9.81
        depression_m = reading["depression"] / 100
        length_m = length / 100
        I_m4 = I / 100000000
        
        if depression_m != 0:
            if bending_type == 1:  # Uniform
                w = force_N / length_m
                Y = (5 * w * length_m**4) / (384 * I_m4 * abs(depression_m))
            else:  # Non-uniform
                Y = (force_N * length_m**3) / (48 * I_m4 * abs(depression_m))
            Y_GPa = Y / 1e9
        else:
            Y_GPa = 0
        
        print(f"{reading['reading_num']:<10} {reading['weight']:<15.2f} "
              f"{reading['depression']:<20.4f} {Y_GPa:<20.2f}")
    
    print("-"*80)
    
    # Final Results
    print("\n" + "="*80)
    print("FINAL YOUNG'S MODULUS (Calculated Average)")
    print("="*80)
    print(f"\n  Calculated Young's Modulus: {calculated_modulus:.2f} GPa")
    print(f"  Expected Young's Modulus:   {material['youngs_modulus']} GPa")
    
    # Calculate percentage difference
    if material['youngs_modulus'] != 0:
        percent_diff = abs(calculated_modulus - material['youngs_modulus']) / material['youngs_modulus'] * 100
        print(f"  Percentage Difference:       {percent_diff:.2f}%")
    
    print("\n" + "="*80)
    
    # Analysis
    print("\nANALYSIS:")
    if abs(calculated_modulus - material['youngs_modulus']) / material['youngs_modulus'] < 0.2:
        print("  ✓ Results are consistent with expected values for this material.")
    else:
        print("  ⚠ Results differ significantly from expected values.")
        print("    Possible reasons: measurement errors, material impurities,")
        print("    temperature effects, or non-ideal experimental conditions.")
    
    print("\n" + "="*80)


def main():
    """Main program function"""
    print("="*80)
    print("YOUNG'S MODULUS MEASUREMENT SYSTEM")
    print("For Thin Sheet-Like Rod Materials")
    print("="*80)
    
    # Get material selection
    material_key, material = get_material_choice()
    
    # Get rod dimensions
    length, breadth, width = get_dimensions()
    
    # Get bending type
    bending_type = get_bending_type()
    
    # Get readings
    readings, weight_increment = get_readings()
    
    # Calculate Young's modulus
    if bending_type == 1:
        calculated_modulus = calculate_youngs_modulus_uniform(
            length, breadth, width, readings
        )
    else:
        calculated_modulus = calculate_youngs_modulus_nonuniform(
            length, breadth, width, readings
        )
    
    # Display results
    display_results(
        material_key, material, length, breadth, width,
        bending_type, readings, calculated_modulus
    )
    
    # Save option
    print("\nWould you like to save these results to a file? (yes/no): ", end="")
    save_choice = input().strip().lower()
    
    if save_choice in ['yes', 'y']:
        filename = f"youngs_modulus_{material_key}_{bending_type}.txt"
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("YOUNG'S MODULUS CALCULATION RESULTS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Material: {material['name']}\n")
            f.write(f"Expected Young's Modulus: {material['youngs_modulus']} GPa\n")
            f.write(f"Calculated Young's Modulus: {calculated_modulus:.2f} GPa\n\n")
            f.write(f"Rod Dimensions: L={length}cm, B={breadth}cm, W={width}cm\n")
            f.write(f"Bending Type: {'Uniform' if bending_type == 1 else 'Non-Uniform'}\n\n")
            f.write("Readings:\n")
            for reading in readings:
                f.write(f"  {reading['reading_num']}: Weight={reading['weight']}g, "
                       f"Depression={reading['depression']}cm\n")
        
        print(f"\n✓ Results saved to {filename}")
    
    print("\nThank you for using the Young's Modulus Measurement System!")
    print("="*80)


if __name__ == "__main__":
    main()