/* eslint-disable no-unused-vars */
import React from 'react'

function priceEstimator(formData) {
    const matCostPerSquareMeter = 10;
    const sittingRoomCostPerSqueareArea = 10;
    const bathRoomCostPerRoom = 10;
    const kitchenRoomCostPerSqueareArea = 10;

    let totalSittingRoomCost = formData.sittingRoomArea * sittingRoomCostPerSqueareArea;
    let totalBathRoomCost = formData.numberOfBathrooms * bathRoomCostPerRoom;
    let totalKitchenCost = formData.kitchenArea * kitchenRoomCostPerSqueareArea;
    let totalMatsCost = 0;

    if (formData.matsToWash) {
      console.log('There are mats to be washed');

      for (let i = 0; i < formData.matsToWash.length; i++) {
        const mat = formData.matsToWash[i];
        // Calculate the cost for this mat
        const matCost = mat.number * mat.area * matCostPerSquareMeter;
        // Add the mat cost to the total cost
        totalMatsCost += matCost;
      }
      console.log("Total cost for mats is: ", totalMatsCost);
    } else {
        console.log('There are no mats found')
    }
    const totalPrice =
      totalMatsCost + totalSittingRoomCost +
      totalBathRoomCost +
      totalKitchenCost;

    return totalPrice;
}
export default function BookingForm() {
    const formData = {
      sittingRoomArea: 12,
      numberOfBathrooms: 4,
      numberofBedRooms: 4,
      kitchenArea: 354,
      matsToWash: [
        {
          number: 1,
          area: 239,
        },
        {
          number: 5,
          area: 200,
        },
        {
          number: 1,
          area: 100000,
        },
      ],
    };
    const estimatedPrice = priceEstimator(formData);
  return (
      <div>
        <div className="flex items-center justify-center p-12">
            <div className="mx-auto w-full max-w-[550px] bg-white">
                <form>
                    <div className="mb-5">
                        <label htmlFor="name" className="mb-3 block text-base font-medium text-[#07074D]">
                            Full Name - {estimatedPrice}
                        </label>
                        <input type="text" name="name" id="name" placeholder="Full Name"
                            className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                    </div>
                    <div className="mb-5">
                        <label htmlFor="phone" className="mb-3 block text-base font-medium text-[#07074D]">
                            Phone Number
                        </label>
                        <input type="text" name="phone" id="phone" placeholder="Enter your phone number"
                            className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                    </div>
                    <div className="mb-5">
                        <label htmlFor="email" className="mb-3 block text-base font-medium text-[#07074D]">
                            Email Address
                        </label>
                        <input type="email" name="email" id="email" placeholder="Enter your email"
                            className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                    </div>
                    <div className="-mx-3 flex flex-wrap">
                        <div className="w-full px-3 sm:w-1/2">
                            <div className="mb-5">
                                <label 
                                    htmlFor="date" 
                                    className="mb-3 block text-base font-medium text-[#07074D]"
                                >
                                    Date
                                </label>
                                <input 
                                    type="date" 
                                    name="date" 
                                    id="date"
                                    className="w-full rounded-md border border-[#e0e0e0] bg-white 
                                    py-3 px-6 text-base font-medium text-[#6B7280]
                                    outline-none focus:border-[#6A64F1] focus:shadow-md"
                                    min={new Date().toISOString().split("T")[0]} // Disable past dates
                                />
                            </div>
                        </div>
                        <div className="w-full px-3 sm:w-1/2">
                            <div className="mb-5">
                                <label htmlFor="time" className="mb-3 block text-base font-medium text-[#07074D]">
                                    Time
                                </label>
                                <input 
                                    type="time" 
                                    name="time" 
                                    id="time"
                                    className="w-full rounded-md border border-[#e0e0e0] bg-white 
                                    py-3 px-6 text-base font-medium text-[#6B7280] outline-none
                                    focus:border-[#6A64F1] focus:shadow-md"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="mb-5 pt-3">
                        <label className="mb-5 block text-base font-semibold text-[#07074D] sm:text-xl">
                            Address Details
                        </label>
                        <div className="-mx-3 flex flex-wrap">
                            <div className="w-full px-3 sm:w-1/2">
                                <div className="mb-5">
                                    <input type="text" name="area" id="area" placeholder="Enter area"
                                        className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                                </div>
                            </div>
                            <div className="w-full px-3 sm:w-1/2">
                                <div className="mb-5">
                                    <input type="text" name="city" id="city" placeholder="Enter city"
                                        className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                                </div>
                            </div>
                            <div className="w-full px-3 sm:w-1/2">
                                <div className="mb-5">
                                    <input type="text" name="state" id="state" placeholder="Enter state"
                                        className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                                </div>
                            </div>
                            <div className="w-full px-3 sm:w-1/2">
                                <div className="mb-5">
                                    <input type="text" name="post-code" id="post-code" placeholder="Post Code"
                                        className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div>
                        <button
                            className="hover:shadow-form w-full rounded-md bg-[#6A64F1] py-3 px-8 text-center text-base font-semibold text-white outline-none">
                            Book Appointment
                        </button>
                    </div>
                </form>
            </div>
        </div>
      </div>
  )
}
